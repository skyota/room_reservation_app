from django.test import TestCase

from .views import HomeView, RoomView

class HomePageTest(TestCase):
    def test_home_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_home_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "reservation/home.html")
        
class RoomPageTest(TestCase):
    def test_room_page_uses_expected_template(self):
        response = self.client.get("/room/")
        self.assertTemplateUsed(response, "reservation/room.html")
