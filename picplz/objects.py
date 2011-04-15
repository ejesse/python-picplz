import datetime


class PicplzObject():
    api = None
    
    @classmethod
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
    
    @classmethod
    def map(self, api, data):
        """map a JSON object into a model instance."""
        self.api=api
        self.name=data['name']
        self.url=data['img_url']
        self.width=int(data['width'])
        self.height = int(data['height'])
        
    def __to_string__(self):
        return self.name

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
    
    def __to_string__(self):
        return self.description

    def from_dict(api,data):
        new_object = PicplzFilter()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)

class UploadPic(PicplzObject):
    file = None
    caption = None
    filter = None
    share_twitter = False
    share_facebook = False
    share_tumblr = False
    share_posterous = False
    share_flickr = False
    share_dropbox = False
    latitude = None
    longitude = None
    horizontal_accuracy = None
    vertical_accuracy = None
    altitude = None
    suppress_sharing = False

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
    
    @classmethod
    def map(self, api, data):
        """map a JSON object into a model instance."""
        self.view_count = int(data['view_count'])
        self.url = data['url']
        self.caption = data['caption']
        self.comment_count = data['comment_count']
        self.like_count = data['like_count']
        self.id = int(data['id'])
#        self.date = datetime.datetime(data['date'])
        pic_files = {}
        pic_files_dict = {}
        for key in data['pic_files'].keys():
            pic_files_dict['name'] = key
            pic_files_dict['img_url'] = data['pic_files'][key]['img_url']
            pic_files_dict['height'] = data['pic_files'][key]['height']
            pic_files_dict['width'] = data['pic_files'][key]['width'] 
            pic_files[pic_files_dict['name']] = PicplzImageFile().from_dict(api, pic_files_dict)
        self.pic_files = pic_files
        creator_data = data['creator']
        self.creator = PicplzUser.from_dict(api, creator_data)
        try:
            city_data = data['city']
            self.city = PicplzCity.from_dict(api, city_data)
        except:
            ## no city, no biggie
            pass
        try:
            place_data = data['place']
            #self.place = PicplzPlace.from_dict(self, api, place_data)
        except:
            ## no place, no biggie
            pass
        
        
    def __to_string__(self):
        return self.caption

    def from_dict(api,data):
        new_object = Pic()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)


            
        

class PicplzUser(PicplzObject):
    username = None
    display_name = None
    following_count = 0
    follower_count = 0
    id = None
    icon = None
    
    @classmethod
    def map(self, api, data):
        self.username = data['username']
        self.display_name = data['display_name']
        self.follower_count = data['follower_count']
        self.following_count = data['following_count']
        self.id = int(data['id'])
        icon_data = data['icon']
        pic_files_dict = {}
        pic_files_dict['name'] = 'icon'
        pic_files_dict['img_url'] = icon_data['url']
        pic_files_dict['height'] = icon_data['height']
        pic_files_dict['width'] = icon_data['width'] 
        self.icon = PicplzImageFile.from_dict(api, pic_files_dict)

    def __to_string__(self):
        return "%s <%s>" % (self.display_name, self.username)

    def from_dict(api,data):
        new_object = PicplzUser()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)

            

class PicplzComment(PicplzObject):
    pass

class PicplzPlace(PicplzObject):
    pass
    
class PicplzCity(PicplzObject):
    
    url = None
    id = None
    name = None
    
    @classmethod
    def map(self, api, data):
        self.url = data['url']
        self.id = int(data['id'])
        self.name = data['name']
    
    def __to_string__(self):
        return self.name

    def from_dict(api,data):
        new_object = PicplzCity()
        new_object.map(api,data)
        return new_object
        
    from_dict = staticmethod(from_dict)
    