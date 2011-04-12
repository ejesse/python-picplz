from picplz.objects import PicplzUser, PicplzPlace, PicplzComment, Pic, PicplzCity
from picplz.errors import PicplzError
import urllib,urllib2,cgi

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
    
    def init(self,authenticator=None):
        if authenticator is not None:
            self.authenticator = authenticator
            
    def __make_unauthenticated_request__(self,endpoint,params_dict):
        
        params = urllib.urlencode(params_dict)
        full_uri = "%s?%s" % (endpoint,params)
        response = urllib2.urlopen(full_uri)
        return response.read()
    
    def __make_authenticated_post__(self,endpoint,params_dict): 

        params = urllib.urlencode(params_dict)
        data = urllib.urlencode(params)
        request = urllib2.Request(endpoint, data)
        response = urllib2.urlopen(request)
        return response.read()
        
    def __make_authenticated_put__(self,endpoint,params_dict):
        
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        params = urllib.urlencode(params_dict)
        data = urllib.urlencode(params)
        request = urllib2.Request(endpoint, data)
        request.get_method = lambda: 'PUT'
        response = opener.open(request)
        return response.read()
        
    def __make_authenticated_delete__(self,endpoint,params_dict): 

        opener = urllib2.build_opener(urllib2.HTTPHandler)
        params = urllib.urlencode(params_dict)
        data = urllib.urlencode(params)
        request = urllib2.Request(endpoint, data)
        request.get_method = lambda: 'DELETE'
        response = opener.open(request)
        return response.read()
        
    def get_feed(self,type,pic_formats=None,pic_page_size=None):
        
        return None
    
    def get_pics(self,ids=None,place=None,user=None):
        
        if (id is None and place is None and user is None):
            raise PicplzError("get_pic method requires one of: a comma delimited list of pic ids, a PicplzPlace, or PicplzUser")
        
        
        pics = []
        
        return pics
        
    def get_pic(self,id=None,longurl_id=None,shorturl_id=None,include_comments=False):
        """" get individual pic, requires one of id, longurl_id, or shorturl_id"""
        
        if (id is None and longurl_id is None and shorturl_id is None):
            raise PicplzError("get_pic method requires one of a pic id, longurl_id or shorturl_id")
        
        return None

    def like_pic(self):
        
        if self.authenticator is None:
            raise PicplzError("like_pic requires an authenticated API instance")
        
        return None
    
    def unlike_pic(self):
        
        if self.authenticator is None:
            raise PicplzError("unlike_pic requires an authenticated API instance")
        
        return None
    
    def comment(self):
        
        if self.authenticator is None:
            raise PicplzError("comment requires an authenticated API instance")
        
        return None
        
    def get_user(self, username=None,id=None,include_detail=False,include_pics=False,pic_page_size=None):
        """ get user info, requires either username or the user's picplz id"""
        
        user = PicplzUser()
        
        return user
        
    def is_authenticated_user_following(self, username=None,id=None):
        """ query whether or not the currently authenticated user is following another user
        requires either username or id of the followee user"""
        if self.authenticator is None:
            raise PicplzError("is_authenticated_user_following requires an authenticated API instance")
        
        return None
        
    def follow_user(self,username=None,id=None):
        
        if self.authenticator is None:
            raise PicplzError("follow_user requires an authenticated API instance")
        
        return None
        
    def unfollow_user(self,username=None,id=None):

        if self.authenticator is None:
            raise PicplzError("unfollow_user requires an authenticated API instance")
        
        return None
        
    def get_place(self,id=None,slug=None,include_detail=False,include_pics=False,pic_page_size=None):
        
        place = PicplzPlace()
        
        return place
    
    def get_city(self,id=None,slug=None,include_detail=False,include_pics=False,pic_page_size=None):
        
        place = PicplzCity()
        
        return place
        