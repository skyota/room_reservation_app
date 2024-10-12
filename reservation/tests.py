from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import json

from .views import *
from .models import *

User = get_user_model()

class HomePageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="testpassword",
        )
        
        self.client.force_login(self.user)
    
    def test_home_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertContains(response, "ゼミ室一覧", status_code=200)
    
    def test_home_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "reservation/home.html")
        
class RoomPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="testpassword",
        )
        
        self.room = Room.objects.create(
            name="2階ゼミ室"
        )
        
        start_time = timezone.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        self.reservation = Reservation.objects.create(
            room=self.room,
            user=self.user,
            title="ゼミ",
            username="山田太郎",
            laboratory="山田研究室",
            start_time=start_time,
            end_time=end_time,
        )
        
        self.factory = RequestFactory()
        self.client.force_login(self.user)
        
    def test_room_page_returns_200_and_expected_title(self):
        response = self.client.get("/room/%s/" % self.room.id)
        self.assertContains(response, self.room.name, status_code=200)
    
    def test_room_page_uses_expected_template(self):
        response = self.client.get("/room/%s/" % self.room.id)
        self.assertTemplateUsed(response, "reservation/room.html")

    def test_should_return_room(self):
        request = RequestFactory().get(f"/room/{self.room.pk}/")
        request.user = self.user
        response = RoomView.as_view()(request, pk=self.room.pk)
        self.assertContains(response, self.room.name, count=4)
        
    def test_should_display_reservation_info(self):
        url = reverse('get_reservations', kwargs={'pk': self.room.pk})

        response = self.client.get(url, {
            'start_date': (timezone.now() + timedelta(days=1)).isoformat(),
            'end_date': (timezone.now() + timedelta(days=2)).isoformat(),
        })

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), 1)

        reservation_data = response_json[0]
        self.assertEqual(reservation_data['title'], "ゼミ")
        self.assertEqual(reservation_data['username'], "山田太郎")
        self.assertEqual(reservation_data['laboratory'], "山田研究室")
        self.assertEqual(reservation_data['start'], self.reservation.start_time.isoformat())
        self.assertEqual(reservation_data['end'], self.reservation.end_time.isoformat())

class AddReservationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="testpassword",
        )
        self.client.force_login(self.user)

        self.room = Room.objects.create(
            name="2階ゼミ室"
        )

        self.start_time = (timezone.now() + timedelta(days=1)).isoformat()
        self.end_time = (timezone.now() + timedelta(days=1, hours=1)).isoformat()

    def test_add_reservation(self):
        url = reverse('add_reservation', kwargs={'pk': self.room.pk})

        data = {
            'title': 'ゼミ',
            'username': '山田太郎',
            'laboratory': '山田研究室',
            'start_date': self.start_time,
            'end_date': self.end_time
        }

        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        # レスポンスJSONを取得して確認
        response_json = response.json()
        self.assertEqual(response_json['title'], data['title'])
        self.assertEqual(response_json['username'], data['username'])
        self.assertEqual(response_json['laboratory'], data['laboratory'])
        self.assertEqual(response_json['start'], self.start_time)
        self.assertEqual(response_json['end'], self.end_time)

        # データベースに予約が追加されていることを確認
        reservation = Reservation.objects.get(pk=response_json['id'])
        self.assertEqual(reservation.title, data['title'])
        self.assertEqual(reservation.username, data['username'])
        self.assertEqual(reservation.laboratory, data['laboratory'])
        self.assertEqual(reservation.start_time.isoformat(), self.start_time)
        self.assertEqual(reservation.end_time.isoformat(), self.end_time)

class DeleteReservationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="testpassword",
        )

        self.client.force_login(self.user)

        self.room = Room.objects.create(
            name="2階ゼミ室"
        )

        start_time = timezone.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        self.reservation = Reservation.objects.create(
            room=self.room,
            user=self.user,
            title="ゼミ",
            username="山田太郎",
            laboratory="山田研究室",
            start_time=start_time,
            end_time=end_time,
        )

    def test_delete_reservation(self):
        url = reverse('delete_reservation', kwargs={
            'pk': self.room.pk, 
            'reservation_id': self.reservation.pk
        })
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "予約が削除されました")
        self.assertFalse(Reservation.objects.filter(pk=self.reservation.pk).exists())
