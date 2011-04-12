



class PicplzObject():
    
    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

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
    pass

class PicplzUser(PicplzObject):
    pass

class PicplzComment(PicplzObject):
    pass

class PicplzPlace(PicplzObject):
    pass
    
class PicplzCity(PicplzObject):
    pass