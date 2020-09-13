from rest_framework.test import APITestCase
from rest_framework import status
from .models import ReleaseApplication
from user.models import User
from equipment.models import Equipment
from rest_framework.authtoken.models import Token


# Create your tests here.
class ReleaseApplicationTestCase(APITestCase):
    def setUp(self):
        User.objects.create(email='1@qq.com', password='123123', address='12123', phone='15801266030', is_staff=True)
        user_one = User.objects.create(email='123@qq.com', password='123123', address='123123', phone='15801266030', is_renter=True)
        user_two = User.objects.create(email='456@qq.com', password='456456', address='456456', phone='18012357727', is_renter=True)
        equipment_one = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪1'
                                                 , description='1w23', owner=user_one)
        equipment_two = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪2'
                                                 , description='1w23', owner=user_two)
        equipment_three = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪3'
                                                 , description='1w23', owner=user_one, status='UNA')
        equipment_four = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪4'
                                                 , description='1w23', owner=user_two, status='UNA')
        equipment_five = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪5'
                                                  , description='1w23', owner=user_two, status='AVA')
        ReleaseApplication.objects.create(equipment=equipment_one, description='789789', owner=equipment_one.owner)
        ReleaseApplication.objects.create(equipment=equipment_two, description='456456', owner=equipment_two.owner)
        ReleaseApplication.objects.create(equipment=equipment_three, description='123123', owner=equipment_three.owner)
        ReleaseApplication.objects.create(equipment=equipment_four, description='101112', owner=equipment_four.owner)
        ReleaseApplication.objects.create(equipment=equipment_four, description='131415', owner=equipment_four.owner, status='ACC')
        ReleaseApplication.objects.create(equipment=equipment_five, description='161718', owner=equipment_five.owner)

    def test_create_release_application(self):
        data = {
            'equipment': Equipment.objects.get(name='光谱仪1').id,
            'description': '123'
        }

        for user in User.objects.all():
            Token.objects.create(user=user)
        token = Token.objects.get(user=User.objects.get(email='123@qq.com'))
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

        response = self.client.post('/api/v1/release-application/', data, form='json')

        equipment = Equipment.objects.get(name='光谱仪1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('owner'), equipment.owner.id)
        self.assertEqual(equipment.status, 'UNA')

        token = Token.objects.get(user=User.objects.get(email='456@qq.com'))
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data_new = {
            'equipment': Equipment.objects.get(name='光谱仪5').id,
            'description': '123123'
        }
        response = self.client.post('/api/v1/release-application/', data_new, form='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # data_new = {
        #     'equipment': -1,
        #     'description': '123123'
        # }
        # response = self.client.post('/api/v1/release-application/', data_new, form='json')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_approve_release_application(self):
        data = {
            'comments': 'ok'
        }
        for user in User.objects.all():
            Token.objects.create(user=user)
        token = Token.objects.get(user=User.objects.get(email='1@qq.com'))
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        release_id = ReleaseApplication.objects.get(description='123123')
        response = self.client.post('/api/v1/release-application/' + str(release_id) + '/approve/', data)

        release_equipment = ReleaseApplication.objects.get(description='123123').equipment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ReleaseApplication.objects.get(description='123123').status, 'ACC')
        self.assertEqual(release_equipment.status, 'AVA')

        release_id = ReleaseApplication.objects.get(description='131415')
        response = self.client.post('/api/v1/release-application/' + str(release_id) + '/approve/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        release_id = ReleaseApplication.objects.get(description='161718')
        response = self.client.post('/api/v1/release-application/' + str(release_id) + '/approve/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_release_application(self):
        data = {
            'comments': 'too bad'
        }

        for user in User.objects.all():
            Token.objects.create(user=user)
        token = Token.objects.get(user=User.objects.get(email='1@qq.com'))
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

        release_id = ReleaseApplication.objects.get(description='101112')
        response = self.client.post('/api/v1/release-application/' + str(release_id) + '/reject/', data)

        release_equipment = ReleaseApplication.objects.get(description='101112').equipment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ReleaseApplication.objects.get(description='101112').status, 'REJ')
        self.assertEqual(release_equipment.status, 'UNR')

        release_id = ReleaseApplication.objects.get(description='131415')
        response = self.client.post('/api/v1/release-application/' + str(release_id) + '/reject/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        release_id = ReleaseApplication.objects.get(description='161718')
        response = self.client.post('/api/v1/release-application/' + str(release_id) + '/reject/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
