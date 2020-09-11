from rest_framework.test import APITestCase
from rest_framework import status
from .models import Equipment
from user.models import User
import json


# Create your tests here.
class EquipmentTestCase(APITestCase):
    def setUp(self):
        User.objects.create(email='123@qq.com', password='123123', address='123123', phone='15801266030')

    def test_create_equipment(self):
        data = {
            'name': '李祁的airdrops',
            'address': '407A',
            'email': '6242@qq.com',
            'phone': '15801266030',
            'description': '怎么了',
            'owner': 1
        }

        response = self.client.post('/api/v1/equipment/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), 1)
        self.assertEqual(Equipment.objects.get().name, '李祁的airdrops')

