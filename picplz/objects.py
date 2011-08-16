import datetime
from picplz.errors import PicplzError
from picplz.utils import dict_to_object_value
import simplejson
import logging
from picplz import LOG_NAME

log = logging.getLogger(LOG_NAME)

ENCODING="ISO-8859-1"

class Location(object):
    latitude = None
    longitude = None
    
    def __to_string__(self):
        return "Location: latitude: %s longitude: %s" % (self.latitude,self.longitude)

    def __repr__(self):
        return self.__to_string__()

class PicplzObject(object):
    api = None
    
    def map(self, api, data):
        """map a dict object into a model instance."""
        raise NotImplementedError
    
    def parse(self,api,json):
        """map a JSON object into a model instance."""
        raise NotImplementedError
        
    def __to_string__(self):
        return self.__name__()
    
    def __repr__(self):
        return self.__to_string__()

class PicplzImageFile(PicplzObject):
    name = None
    url = None
    width = 0
    height = 0
    
    def map(self, api, data):
        """map a dict object into a model instance."""
        self.api=api
        dict_to_object_value('name', self, data)
        dict_to_object_value('img_url', self, data, object_field_name='url')
        dict_to_object_value('width', self, data, type='int')
        dict_to_object_value('height', self, data, type='int')
        
        self.name=data['name']
        self.url=data['img_url']
        self.width=int(data['width'])
        self.height = int(data['height'])
        
    def __to_string__(self):
        return self.name.encode('utf-8')

    def from_dict(api,data):
        new_object = PicplzImageFile()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)

class PicplzFilter(PicplzObject):
    
    id = None
    description = None
    
    def __init__(self,id=None,description=None):
        self.id=id
        self.description=description    
    
    def map(self, api, data):
        dict_to_object_value('id',self,data)
        dict_to_object_value('description',self,data)
    
    def __to_string__(self):
        return self.description.encode('utf-8')

    def from_dict(api,data):
        new_object = PicplzFilter()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)

class UploadPic(PicplzObject):
    file = None
    caption = None
    filter = None
    share_twitter = None
    share_facebook = None
    share_tumblr = None
    share_posterous = None
    share_flickr = None
    share_dropbox = None
    latitude = None
    longitude = None
    horizontal_accuracy = None
    vertical_accuracy = None
    altitude = None
    suppress_sharing = False
    
    def __to_string__(self):
        return self.caption
    
    def __make_it_bin__(self,value):
        if value:
            return 1
        else:
            return 0
    
    def get_parameters(self):
        params ={}
        if self.caption is not None:
            params['caption'] = self.caption
        if self.filter is not None:
            params['filter'] = self.filter.id
        if self.share_twitter is not None:
            params['share_twitter'] = self.__make_it_bin__(self.share_twitter)
        if self.share_facebook is not None:
            params['share_facebook'] = self.__make_it_bin__(self.share_facebook)
        if self.share_tumblr is not None:
            params['share_tumblr'] = self.__make_it_bin__(self.share_tumblr)
        if self.share_posterous is not None:
            params['share_posterous'] = self.__make_it_bin__(self.share_posterous)
        if self.share_flickr is not None:
            params['share_flickr'] = self.__make_it_bin__(self.share_flickr)
        if self.share_dropbox is not None:
            params['share_dropbox'] = self.__make_it_bin__(self.share_dropbox)
        if self.latitude is not None:
            params['latitude'] = self.latitude
        if self.longitude is not None:
            params['longitude'] = self.longitude
        if self.horizontal_accuracy is not None:
            params['horizontal_accuracy'] = self.horizontal_accuracy
        if self.vertical_accuracy is not None:
            params['vertical_accuracy'] = self.vertical_accuracy
        if self.altitude is not None:
            params['altitude'] = self.altitude
        if self.suppress_sharing is not None:
            params['suppress_sharing'] = self.__make_it_bin__(self.suppress_sharing)
        return params

class Pic(PicplzObject):
    creator = None
    view_count = 0
    url = None
    pic_files = []
    caption = None
    comment_count = 0
    like_count = 0
    date = None
    id = None
    city=None
    place=None
    comments=[]
    location=None
    api=None
    
    def init(self,api=None,data=None):
        if api is not None:
            self.api = api
        if data is not None:
            self.map(api,data)
    
    def map(self, api, data):
        self.api = api
        """map a JSON object into a model instance."""
        dict_to_object_value('view_count', self, data, type='int')
        dict_to_object_value('url', self, data)
        dict_to_object_value('caption', self, data)
        dict_to_object_value('comment_count', self, data, type='int')
        dict_to_object_value('like_count', self, data, type='int')
        dict_to_object_value('id', self, data, type='int')
        dict_to_object_value('date', self, data, type='datetime')
        
        ## this is confusing, just go with it
        pic_files = {}
        pic_files_dict = {}
        for key in data['pic_files'].keys():
            pic_dict = data['pic_files'][key]
            pic_files_dict['name'] = key
            pic_files_dict['img_url'] = pic_dict['img_url']
            pic_files_dict['height'] = pic_dict['height']
            pic_files_dict['width'] = pic_dict['width'] 
            pic_files[pic_files_dict['name']] = PicplzImageFile().from_dict(api, pic_files_dict)
        self.pic_files = pic_files
        
        
        try:
            creator_data = data['creator']
            self.creator = PicplzUser.from_dict(api, creator_data)
        except:
            pass
        try:
            city_data = data['city']
            self.city = PicplzCity.from_dict(api, city_data)
        except:
            ## no city, no biggie
            pass
        
        if data.has_key('location'):
            self.location = Location()
            dict_to_object_value('lat', self.location, data['location'],object_field_name='latitude')
            dict_to_object_value('lon', self.location, data['location'],object_field_name='longitude')

        try:
            place_data = data['place']
            self.place = PicplzPlace.from_dict(api, place_data)
        except:
            ## no place, no biggie
            pass
        try:
            comment_string = data['items']
            for item in comment_string:
                comment=PicplzComment.from_dict(api, item)
                self.comments.append(comment)
        except:
            pass
        
        
    def __to_string__(self):
        return self.caption.encode('utf-8')

    def from_dict(api,data):
        new_object = Pic()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)
    
    def like(self):
        """ convenience method """
        return self.api.like_pic(pic=self)
    
    def unlike(self):
        return self.api.unlike_pic(pic=self)

class PicplzUser(PicplzObject):
    username = None
    display_name = None
    following_count = 0
    follower_count = 0
    id = None
    icon = None
    pics = None
    __has_more_pics__=False
    __last_pic_id__=False
    
    def __init__(self,api=None):
        self.api = api
    
    def map(self, api, data):
        self.api = api
        dict_to_object_value('username', self, data)
        dict_to_object_value('display_name', self, data)
        dict_to_object_value('id', self, data)
        dict_to_object_value('follower_count', self, data,type='int')
        dict_to_object_value('following_count', self, data,type='int')
        try:
            self.pics = {}
            __has_more_pics__=False
            __last_pic_id__=False
            icon_data = data['icon']
            pic_files_dict = {}
            pic_files_dict['name'] = 'icon'
            pic_files_dict['img_url'] = icon_data['url']
            pic_files_dict['height'] = icon_data['height']
            pic_files_dict['width'] = icon_data['width'] 
            self.icon = PicplzImageFile.from_dict(api, pic_files_dict)
        except:
            pass
        try:
            pics_data = data['pics']
            for pic_data in pics_data:
                next_pic = Pic()
                next_pic = Pic.from_dict(self.api,pic_data)
                self.pics[next_pic.id] = next_pic
        except:
            ## no pics :(
            pass

    def __to_string__(self):
        return "%s <%s>" % (self.display_name, self.username)

    def __fetch_pics__(self,go_back_for_more=False,last_pic_id=None):
        if not self.api:
            raise PicplzError("Objects must have been instantiated with no API. Without an API the object cannot fetch anything :(")
        if go_back_for_more:
            # NomNomNomNomNomNomNomNomNom
            pics_user = self.api.get_user(username=self.username,include_pics=True,last_pic_id=last_pic_id,pic_page_size=100)
        else:
            pics_user = self.api.get_user(username=self.username,include_pics=True,last_pic_id=last_pic_id)
        for pic_key in pics_user.pics.keys():
            self.pics[pic_key] = pics_user.pics[pic_key]
            self.pics[pic_key].creator = self
        if go_back_for_more:
            if pics_user.__has_more_pics__:
                # recursion FTW
                # NomNomNomNomNomNomNomNomNom
                return self.__fetch_pics__(go_back_for_more=True,last_pic_id=pics_user.__last_pic_id__)
        return self.pics

    def fetch_pics(self):
        return self.__fetch_pics__()
        
    def fetch_all_pics(self):
        return self.__fetch_pics__(go_back_for_more=True)

    def from_dict(api,data):
        new_object = PicplzUser(api=api)
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)

            

class PicplzComment(PicplzObject):
    
    content = None
    user = None
    comement_id = None
    pic = None
    date = None
    
    def map(self, api, data):
        dict_to_object_value('id', self, data)
        dict_to_object_value('content', self, data)
        dict_to_object_value('date', self, data,type='datetime')
        try:
            user_data = data['user']
            self.creator = PicplzUser.from_dict(api, user_data)
        except:
            pass
    
    def __to_string__(self):
        return self.content.encode('utf-8')
    
    def from_dict(api,data):
        new_object = PicplzComment()
        new_object.map(api,data)
        return new_object
    
    from_dict = staticmethod(from_dict)

class PicplzPlace(PicplzObject):
    
    url = None
    id = None
    name = None
    pics = None
    
    def map(self, api, data):
        dict_to_object_value('id', self, data)
        dict_to_object_value('url', self, data)
        dict_to_object_value('name', self, data)
        try:
            pics_data = data['pics']
            self.pics={}
            for pic_data in pics_data:
                next_pic = Pic()
                next_pic = Pic.from_dict(self.api,pic_data)
                self.pics[next_pic.id] = next_pic
        except:
            ## no pics :(
            pass        
    
    def __to_string__(self):
        return self.name.encode('utf-8')

    def from_dict(api,data):
        new_object = PicplzPlace()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)
    
class PicplzCity(PicplzObject):
    
    url = None
    id = None
    name = None
    pics = None

    def map(self, api, data):
        dict_to_object_value('id', self, data)
        dict_to_object_value('url', self, data)
        dict_to_object_value('name', self, data)
        try:
            pics_data = data['pics']
            self.pics={}
            for pic_data in pics_data:
                next_pic = Pic()
                next_pic = Pic.from_dict(self.api,pic_data)
                self.pics[next_pic.id] = next_pic
        except:
            ## no pics :(
            pass
    
    def __to_string__(self):
        return self.name.encode('utf-8')

    def from_dict(api,data):
        new_object = PicplzCity()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)
    
class PicplzLike(PicplzObject):
    
    date = None
    id = None
    picplz_type = 'like'
    user = None
    
    def map(self, api, data):
        dict_to_object_value('id', self, data)
        dict_to_object_value('date', self, data,type='datetime')
        self.user = PicplzUser.from_dict(api, data['user'])
    
    def __to_string__(self):
        return "Picplz Like with id: %s" % (self.id)

    def from_dict(api,data):
        new_object = PicplzLike()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)
    