from rest_framework.test import APITestCase
from rest_framework import status
from .models import ReleaseApplication
from user.models import User
from equipment.models import Equipment


# Create your tests here.
class ReleaseApplicationTestCase(APITestCase):
    def setUp(self):
        user_one = User.objects.create(email='123@qq.com', password='123123', address='123123', phone='15801266030')
        user_two = User.objects.create(email='456@qq.com', password='456456', address='456456', phone='18012357727')
        equipment_one = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪1'
                                                 , description='1w23', owner=user_one)
        equipment_two = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪2'
                                                 , description='1w23', owner=user_two)
        ReleaseApplication.objects.create(equipment=equipment_one, description='789789', owner=equipment_one.owner)
        ReleaseApplication.objects.create(equipment=equipment_two, description='456456', owner=equipment_two.owner)

    def test_create_release_application(self):
        data = {
            'equipment': Equipment.objects.get(name='光谱仪1').id,
            'description': '123123'
        }

        response = self.client.post('/api/v1/release-application/', data, form='json')

        equipment = Equipment.objects.get(name='光谱仪1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('owner'), equipment.owner.id)
        self.assertEqual(equipment.status, 'UNA')

    def test_approve_release_application(self):
        data = {
            'comments': 'ok'
        }

        release_id = ReleaseApplication.objects.get(description='789789')
        response = self.client.post('/api/v1/release-application/' + str(release_id) + '/approve/', data)

        release_equipment = release_id.equipment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'ACC')
        self.assertEqual(release_equipment.status, 'AVA')

    def test_reject_release_application(self):
        data = {
            'comments': 'too bad'
        }

        release_id = ReleaseApplication.objects.get(description='456456')
        response = self.client.post('/api/v1/release-application/' + str(release_id) + '/reject/', data)

        release_equipment = release_id.equipment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'REJ')
        self.assertEqual(release_equipment.status, 'UNR')
