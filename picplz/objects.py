



class PicplzObject():
    
    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError
    
class Pic(PicplzObject):
    pass

class PicplzUser(PicplzObject):
    pass

class Comment(PicplzObject):
    pass

class Place(PicplzObject):
    pass
    
class City(PicplzObject):
    pass