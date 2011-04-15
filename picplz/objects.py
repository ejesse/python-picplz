import datetime


class PicplzObject():
    api = None
    
    def parse(self, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

class PicplzImageFile(PicplzObject):
    name = None
    url = None
    width = 0
    height = 0
    
    def parse(self, api, data):
        """Parse a JSON object into a model instance."""
        self.api=api
        self.name=data['name']
        self.url=data['img_url']
        self.width=int(data['width'])
        self.height = int(data['height'])
    
    
class PicplzFilter(PicplzObject):
    
    id = None
    description = None
    
    def __init__(self,id=None,description=None):
        self.id=id
        self.description=description    
    
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
    
    @classmethod
    def parse(self, api, data):
        """Parse a JSON object into a model instance."""
        self.view_count = int(data['view_count'])
        self.url = data['url']
        self.caption = data['caption']
        self.comment_count = data['comment_count']
        self.like_count = data['like_count']
        self.id = data['id']
#        self.date = datetime.datetime(data['date'])
        pic_files = []
        pic_files_dict = {}
        for key in data['pic_files'].keys():
            pic_files_dict['name'] = key
            pic_files_dict['img_url'] = data['pic_files'][key]['img_url']
            pic_files_dict['height'] = data['pic_files'][key]['height']
            pic_files_dict['width'] = data['pic_files'][key]['width'] 
            picplz_image_file = PicplzImageFile()
            picplz_image_file.parse(api, pic_files_dict)
            pic_files.append(picplz_image_file)
        self.pic_files = pic_files
        
        ##TODO FIXME need to map creator next
        ## pt 2: this is hacky/klugey need real parsing
            
        

class PicplzUser(PicplzObject):
    username = None
    display_name = None
    following_count = 0
    follower_count = 0
    id = None

class PicplzComment(PicplzObject):
    pass

class PicplzPlace(PicplzObject):
    pass
    
class PicplzCity(PicplzObject):
    pass