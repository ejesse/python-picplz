from cStringIO import StringIO
from picplz.errors import PicplzError
from picplz.helpers import MultiPartForm
from picplz.objects import PicplzUser, PicplzPlace, PicplzComment, Pic, \
    PicplzCity, PicplzFilter, UploadPic, PicplzLike
from picplz.utils import to_unicode_or_bust
from picplz.authentication import PicplzAuthenticator,PicplzOauthToken
import cgi
import simplejson
import urllib
import urllib2
import httplib2
import logging
from picplz import LOG_NAME

log = logging.getLogger(LOG_NAME)

class PicplzAPI():
    """ picplz API """
    
    authenticator = None
    api_base = 'https://api.picplz.com/api/v2'
    feed_endpoint = api_base + '/feed.json'
    pic_endpoint = api_base + '/pic.json'
    like_endpoint = api_base + '/pic/like.json'
    comment_endpoint = api_base + '/pic/comment.json'
    user_endpoint = api_base + '/user.json'
    follow_endpoint = api_base + '/user/follow.json'
    place_endpoint = api_base + '/place.json'
    city_endpoint = api_base + '/city.json'
    filters_endpoint = api_base + '/filters.json'
    upload_endpoint = api_base + '/upload_basic.json'
    print_json = False
    authenticated_user = None
    is_authenticated = False
    
    def __init__(self,picplz_client_id=None,picplz_client_secret=None,registered_redirect_uri=None,authenticator=None, print_json=False, access_token=None, access_token_string=None):
        if access_token_string is not None:
            access_token = PicplzOauthToken.from_string(access_token_string)
        if authenticator is not None:
            self.authenticator = authenticator
        if picplz_client_id is not None and picplz_client_secret is not None and registered_redirect_uri is not None:
            if access_token is not None:
                self.authenticator = PicplzAuthenticator(picplz_client_id,picplz_client_secret,registered_redirect_uri,access_token=access_token)
            else:
                self.authenticator = PicplzAuthenticator(picplz_client_id,picplz_client_secret,registered_redirect_uri)
        self.print_json = print_json
        
        if self.authenticator is not None:
            if self.authenticator.access_token is not None:
                ## go get authenticated user's info
                self.authenticated_user = self.get_user(id='self')
                self.is_authenticated = True
        

    def __check_for_picplz_error__(self,json):
        error_text = 'Unknown picplz error'
        result = simplejson.loads(json)
        if result.has_key('result'):
            if result['result'] == "error":
                if result.has_key('text'): 
                    error_text = result['text']
                raise PicplzError('An error was returned from PicPlz API: %s' % (error_text))
            
    def __make_unauthenticated_get__(self,endpoint,params_dict):
        
        params = urllib.urlencode(params_dict)
        full_uri = "%s?%s" % (endpoint,params)
        log.debug("Making unauthenticated get request to %s with parameters %s" % (endpoint,params))
        response = urllib2.urlopen(full_uri)
        response_text = response.read()
        log.debug("Picplz server response: %s" % (response_text))
        response_text = to_unicode_or_bust(response_text, 'iso-8859-1')
        #self.__check_for_picplz_error__(response_text)
        return response_text
    
    def __make_authenticated_request__(self,endpoint,params_dict,method='POST'):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        params = params_dict
        params['oauth_token'] = self.authenticator.access_token.to_string()
        
        http = httplib2.Http()
        
        headers = {'Content-type': 'application/json'}
        
        response = http.request(endpoint,method,headers=headers,body=urllib.urlencode(params))
        
        #data = urllib.urlencode(params)
        #request = urllib2.Request(endpoint, data)
        #request.get_method = lambda: method
        #request.add_header('Content-Type', 'text/json')
        #if method.lower() == 'get' or method.lower() == 'delete':
        #    params = urllib.urlencode(params)
        log.debug("Making authenticated %s request to %s with parameters %s" % (method,endpoint,params))
        #response = opener.open(request)
        #response_text = response.read()
        #log.debug("API Response info %s" % (response)
 #       log.debug("API Response headers %s" % (response.info().headers))
        log.debug("Picplz server response: %s" % (response))
        cleaned_response = to_unicode_or_bust(response, 'iso-8859-1')
        #self.__check_for_picplz_error__(response_text)
        return cleaned_response
    
    def __make_authenticated_get__(self,endpoint,params_dict): 

        return self.__make_authenticated_request__(endpoint,params_dict, 'GET')
    
    def __make_authenticated_post__(self,endpoint,params_dict): 

        return self.__make_authenticated_request__(endpoint,params_dict)
        
    def __make_authenticated_put__(self,endpoint,params_dict):
        
        return self.__make_authenticated_request__(endpoint,params_dict,'PUT')
        
    def __make_authenticated_delete__(self,endpoint,params_dict): 

        return self.__make_authenticated_request__(endpoint,params_dict,'DELETE')

    def get_authorization_url(self):
        """ convenenience method """
        return self.authenticator.get_authorization_url()
    
    def get_access_token(self,code=None):
        return self.authenticator.get_access_token(self,code=None)
        
    def get_feed(self,type,pic_formats=None,pic_page_size=None,last_pic_id=False):
        
        parameters = {'type':type}
        if pic_formats is not None:
            parameters['pic_formats']=pic_formats
        if last_pic_id:
            parameters['last_pic_id']=last_pic_id
        if pic_page_size is not None:
            parameters['pic_page_size']=pic_page_size
        
        return self.__make_unauthenticated_get__(self.feed_endpoint, parameters)
    
    def get_filters(self):
        
        parameters={}
        
        returned_json = self.__make_unauthenticated_get__(self.filters_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        filter_data = returned_data['value']['filters']
        filters = []
        for f in filter_data:
            filter = PicplzFilter.from_dict(self, f)
            filters.append(filter)
        return filters
    
    def get_pics(self,ids=None,place=None,user=None,last_pic_id=False):
        
        if (id is None and place is None and user is None):
            if self.authenticated_user is None:
                raise PicplzError("get_pic method requires one of: a comma delimited list of pic ids, a PicplzPlace, or PicplzUser")
            else:
                user = self.authenticated_user
        
        if user is not None:
            return user.fetch_all_pics()
        
        pics = []
        
        return pics
        
    def get_pic(self,id=None,longurl_id=None,shorturl_id=None,include_comments=False):
        """" get individual pic, requires one of id, longurl_id, or shorturl_id"""
        
        if (id is None and longurl_id is None and shorturl_id is None):
            raise PicplzError("get_pic method requires one of a pic id, longurl_id or shorturl_id")
        
        parameters = {}
        if id is not None:
            parameters['id']=id
        if longurl_id is not None:
            parameters['longurl_id']=longurl_id
        if shorturl_id is not None:
            parameters['shorturl_id']=shorturl_id
        if include_comments is not None:
            parameters['include_items']=1
        
        ## for now, include geo data by default
        parameters['include_geo']=1
        
        returned_json = self.__make_unauthenticated_get__(self.pic_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        pic_data = returned_data['value']['pics'][0]
        pic = Pic.from_dict(self,pic_data)

        return pic
    
    def upload_pic(self, upload_pic):
        
        if not self.is_authenticated:
            raise PicplzError("uploading a new pic requires an authenticated API instance")

        parameters = upload_pic.get_parameters()
        
        form = MultiPartForm()
        form.add_field('oauth_token', self.authenticator.access_token.to_string())
        for key in parameters.keys():
            form.add_field(key,parameters[key])
        
        # Add a fake file
        form.add_file('file', upload_pic.file.name, 
                      fileHandle=upload_pic.file)
    
        # Build the request
        request = urllib2.Request(self.upload_endpoint)
        request.add_header('User-agent', 'python-picplz: https://github.com/ejesse/python-picplz')
        body = str(form)
        request.add_header('Content-type', form.get_content_type())
        request.add_header('Content-length', len(body))
        request.add_data(body)
    
        response = urllib2.urlopen(request)
        response_text = response.read()
        if self.print_json:
            print response_text
        self.__check_for_picplz_error__(response_text)
        return response_text
        

    def like_pic(self,pic=None,id=None,longurl_id=None,shorturl_id=None):
        
        if not self.is_authenticated:
            raise PicplzError("like_pic requires an authenticated API instance")
        
        if (pic is None and id is None and longurl_id is None and shorturl_id is None):
            raise PicplzError("like_pic method requires one of a pic id, longurl_id or shorturl_id")
        
        parameters = {}
        if pic is not None:
            parameters['id']=pic.id
        if id is not None:
            parameters['id']=id
        if longurl_id is not None:
            parameters['longurl_id']=longurl_id
        if shorturl_id is not None:
            parameters['shorturl_id']=shorturl_id

        returned_json = self.__make_authenticated_post__(self.like_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        like_data = returned_data['value']['like']
        like = PicplzLike.from_dict(self,like_data)

        return like
    
    def unlike_pic(self, id=None, pic=None):
        if not self.is_authenticated:
            raise PicplzError("unlike_pic requires an authenticated API instance")
        
        if id is None and pic is None:
            raise PicplzError("Pass in a pic object or a pic id, otherwise there's nothing to unlike!")
        
        parameters = {}
        if id is not None:
            parameters['id']=id
        if pic is not None:
            parameters['id']=pic.id
        
        returned_json = self.__make_authenticated_delete__(self.like_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        #like_data = returned_data['value']['like']
        #like = PicplzLike.from_dict(self,like_data)

        return returned_data
    
    def comment(self, comment=None,comment_text=None,id=None,longurl_id=None,shorturl_id=None):
        
        if not self.is_authenticated:
            raise PicplzError("comment requires an authenticated API instance")
        
        parameters = {}
        comment_content=None
        pic_id = None
        
        if comment is None:
            if (id is None and longurl_id is None and shorturl_id is None):
                raise PicplzError("comment method requires one of a pic id, longurl_id or shorturl_id")
            if comment_text is None:
                raise PicplzError("To make a comment you must supply either a PicplzComment object (with the content field set) or pass in a string to comment_text parameter, otherwise what are you commenting?")
            comment_content = comment_text
            if id is not None:
                pic_id=id
            if longurl_id is not None:
                parameters['longurl_id']=longurl_id
            if shorturl_id is not None:
                parameters['shorturl_id']=shorturl_id
        else:
            if comment.content is None:
                raise PicplzError("To make a comment you must supply either a PicplzComment object (with the content field set) or pass in a string to comment_text parameter, otherwise what are you commenting?")
            if comment.pic is None:
                if (id is None and longurl_id is None and shorturl_id is None):
                    raise PicplzError("comment method requires one of a pic id, longurl_id or shorturl_id or setting the pic property on a PizPlzComment object")
            comment_content = comment.content
            pic_id = comment.pic.id
            
        if pic_id is not None:
            parameters['id'] = pic_id
        
        parameters['comment'] = comment_content
        
        returned_json = self.__make_authenticated_post__(self.comment_endpoint, parameters)
        
        returned_data = simplejson.loads(returned_json)
        data = returned_data['value']['comment']
        comment = PicplzComment.from_dict(self, data)
        
        return comment
    
    def delete_comment(self, comment_id=None, comment=None):
        
        if not self.is_authenticated:
            raise PicplzError("deleting a comment requires an authenticated API instance")
        
        if (comment_id is None and comment is None):
            raise PicplzError("In order to delete a comment you must pass in a comment_id or the comment to be deleted")
        
        parameters = {}
        if comment is not None:
            parameters['comment_id'] = comment.id
        else:
            parameters['comment_id'] = comment_id
        
        returned_json = self.__make_authenticated_delete__(self.comment_endpoint, parameters)
        
        returned_data = simplejson.loads(returned_json)
        return returned_data
        
    def get_user(self, username=None,id=None,include_detail=False,include_pics=False,pic_page_size=None,last_pic_id=False):
        """ get user info, requires either username or the user's picplz id"""
        
        if (id is None and username is None):
            if self.authenticator.access_token is not None:
                id = 'self'
            else:
                raise PicplzError("get_user method requires one of a pic id, longurl_id or shorturl_id")
        
        parameters = {}
        if id is not None:
            parameters['id']=id
        if username is not None:
            parameters['username']=username
        if include_detail:
            parameters['include_detail']=1
        if include_pics:
            parameters['include_pics']=1
        if last_pic_id:
            parameters['last_pic_id']=last_pic_id
        if pic_page_size is not None:
            parameters['pic_page_size']=pic_page_size
        
        if id == 'self':
            returned_json = self.__make_authenticated_get__(self.user_endpoint, parameters)
        returned_json = self.__make_unauthenticated_get__(self.user_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        data = returned_data['value']['users'][0]
        user = PicplzUser.from_dict(self, data)
        try:
            has_more_pics = returned_data['value']['users'][0]['more_pics']
            if has_more_pics:
                user.__has_more_pics__ = True
            else:
                user.__has_more_pics__ = False
        except:
            user.__has_more_pics__ = False
        try:
            last_pic_id = returned_data['value']['users'][0]['last_pic_id']
            user.__last_pic_id__ = last_pic_id
        except:
            user.__last_pic_id__ = False
        
        return user
        
    def is_authenticated_user_following(self, username=None,id=None):
        """ query whether or not the currently authenticated user is following another user
        requires either username or id of the followee user"""
        if not self.is_authenticated:
            raise PicplzError("is_authenticated_user_following requires an authenticated API instance")
        
        return None
        
    def follow_user(self,username=None,id=None):
        
        if not self.is_authenticated:
            raise PicplzError("follow_user requires an authenticated API instance")
        
        return None
        
    def unfollow_user(self,username=None,id=None):

        if not self.is_authenticated:
            raise PicplzError("unfollow_user requires an authenticated API instance")
        
        return None
    
    def get_place(self,id=None,slug=None,include_detail=False,include_pics=False,pic_page_size=None):
        
        parameters = {}
        if id is not None:
            parameters['id']=id
        if slug is not None:
            parameters['slug']=slug
        if include_detail:
            parameters['include_detail']=1
        if include_pics:
            parameters['include_pics']=1
        if pic_page_size is not None:
            parameters['pic_page_size']=pic_page_size
        
        returned_json = self.__make_unauthenticated_get__(self.place_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        data = returned_data['value']['places'][0]
        
        place = PicplzPlace.from_dict(self,data)
        
        return place
    
    def get_places(self,ids=None,slugs=None):
        pass
    
    def get_city(self,id=None,slug=None,include_detail=False,include_pics=False,pic_page_size=None):
        
        parameters = {}
        if id is not None:
            parameters['id']=id
        if slug is not None:
            parameters['slug']=slug
        if include_detail:
            parameters['include_detail']=1
        if include_pics:
            parameters['include_pics']=1
        if pic_page_size is not None:
            parameters['pic_page_size']=pic_page_size
        
        returned_json = self.__make_unauthenticated_get__(self.city_endpoint, parameters)
        returned_data = simplejson.loads(returned_json)
        data = returned_data['value']['cities'][0]
        
        city = PicplzCity.from_dict(self,data)
        
        return city
    
    def get_cities(self,ids=None,slugs=None):
        pass
        