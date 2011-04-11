from picplz.objects import PicplzUser, Place


class PicplzAPI():
    """ picplz API """
    
    def get_feed(self,type,pic_formats=None,pic_page_size=None):
        
        return None
    
    def get_pics(self,ids=None,longurl_id=None,shorturl_id=None,place=None,user=None):
        
        pics = []
        
        return pics
        
    def get_pic(self,id=None,longurl_id=None,shorturl_id=None,include_comments=False):
        """" get individual pic, requires one of id, longurl_id, or shorturl_id"""
        
        if (id is None and longurl_id is None and shorturl_id is None):
            return None
        
        return None

    def like_pic(self):
        
        return None
        
    def comment(self):
        
        return None
        
    def get_user(self, username=None,id=None,include_detail=False,include_pics=False,pic_page_size=None):
        """ get user info, requires either username or the user's picplz id"""
        
        user = PicplzUser()
        
        return user
        
    def is_authenticated_user_following(self, username=None,id=None):
        """ query whether or not the currently authenticated user is following another user
        requires either username or id of the followee user"""
        
    def follow_user(self,username=None,id=None):
        
        return None
        
    def unfollow_user(self,username=None,id=None):

        return None
        
    def get_place(self,id=None,slug=None,include_detail=False,include_pics=False,pic_page_size=None):
        
        place = Place()
        
        return place
        