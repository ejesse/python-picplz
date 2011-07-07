import unittest
from picplz.api import PicplzAPI

class PicplzAPITest(unittest.TestCase):
    def setUp(self):
        self.api = PicplzAPI()
        self.api.print_json=True
    
    def test_get_pic(self):
        id = 1534270
        pic = self.api.get_pic(id=id)
        self.assertEqual(pic.id, id)
        
    def test_get_city(self):
        city_id = 3
        city = self.api.get_city(id=city_id)
        self.assertEqual(city.id, city_id)
        
    def test_get_filters(self):
        filters = self.api.get_filters()
        self.assertNotEqual(None,filters)
        
    def test_get_place(self):
        place_id=1
        place = self.api.get_place(id=place_id)
        self.assertEqual(place.id, place_id)

    def test_user(self):
        username = 'ejesse'
        user = self.api.get_user(username)
        self.assertEqual(user.username, username)
#    def test_like_pic(self):

#    def test_unlike_pic(self):


if __name__ == '__main__':
    unittest.main()    