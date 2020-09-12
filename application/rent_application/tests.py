from rest_framework.test import APITestCase
from rest_framework import status
from .models import RentApplication
from user.models import User
from equipment.models import Equipment


# Create your tests here.
class RentApplicationTestCase(APITestCase):
    def setUp(self):
        user_one = User.objects.create(email='123@qq.com', password='123123', address='123123', phone='15801266030')
        user_two = User.objects.create(email='456@qq.com', password='456456', address='456456', phone='18012357727')
        equipment_one = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪1'
                                                 , description='1w23', owner=user_one)
        equipment_two = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪2'
                                                 , description='1w23', owner=user_two)
        equipment_three = Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区'
                                                   , name='光谱仪3 ', description='1w23', owner=user_two, status='RET')
        RentApplication.objects.create(equipment=equipment_one, borrower=user_two, description='789789'
                                       , lease_term_begin='2020-09-20 17:44:25', lease_term_end='2020-10-20 17:44:25')
        RentApplication.objects.create(equipment=equipment_two, borrower=user_one, description='456456'
                                       , lease_term_begin='2020-09-20 17:44:25', lease_term_end='2020-10-20 17:44:25')
        RentApplication.objects.create(equipment=equipment_two, borrower=user_one, description='123123'
                                       , lease_term_begin='2020-09-20 17:44:25', lease_term_end='2020-10-20 17:44:25'
                                       , status='ACC', applying=True)
        RentApplication.objects.create(equipment=equipment_three, borrower=None, description='101112'
                                       , lease_term_begin='2020-09-20 17:44:25', lease_term_end='2020-10-20 17:44:25'
                                       , status='ACC', applying=True)
        RentApplication.objects.create(equipment=equipment_two, borrower=user_one, description='123123UNR'
                                       , lease_term_begin='2020-09-20 17:44:25', lease_term_end='2020-10-20 17:44:25'
                                       , status='UNR', applying=False)
        RentApplication.objects.create(equipment=equipment_two, borrower=user_one, description='123123REJ'
                                       , lease_term_begin='2020-09-20 17:44:25', lease_term_end='2020-10-20 17:44:25'
                                       , status='REJ', applying=False)

    def test_create_rent_application(self):
        data = {
            'equipment': Equipment.objects.get(name='光谱仪1').id,
            'borrower': User.objects.get(email='456@qq.com').id,
            'description': '123123',
            'lease_term_begin': '2020-09-20 17:44:25',
            'lease_term_end': '2020-10-20 17:44:25'
        }

        response = self.client.post('/api/v1/rent-application/', data, form='json')

        equipment = Equipment.objects.get(name='光谱仪1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('renter'), equipment.owner.id)

    def test_approve_rent_application(self):
        data = {
            'comments': 'good job'
        }

        rent_id = RentApplication.objects.get(description='789789')
        response = self.client.post('/api/v1/rent-application/' + str(rent_id) + '/approve/', data)

        rent_equipment = rent_id.equipment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'ACC')
        self.assertEqual(response.data.get('applying'), True)
        self.assertEqual(rent_equipment.status, 'REN')
        self.assertEqual(rent_equipment.borrower, RentApplication.objects.get(description='789789').borrower)

        rent_id = RentApplication.objects.get(description='123123')
        response = self.client.post('/api/v1/rent-application/' + str(rent_id) + '/approve/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        rent_id = RentApplication.objects.get(description='123123REJ')
        response = self.client.post('/api/v1/rent-application/' + str(rent_id) + '/approve/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_rent_application(self):
        data = {
            'comments': 'too bad'
        }

        rent_id = RentApplication.objects.get(description='456456')
        response = self.client.post('/api/v1/rent-application/' + str(rent_id) + '/reject/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'REJ')
        self.assertEqual(response.data.get('applying'), False)

    def test_return_rent_application(self):
        data = {
            'user_comments': 'not bad'
        }

        rent_id = RentApplication.objects.get(description='123123')
        response = self.client.post('/api/v1/rent-application/' + str(rent_id) + '/return/', data)

        rent_equipment = rent_id.equipment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rent_equipment.status, 'RET')
        self.assertEqual(rent_equipment.borrower, None)

    def test_return_confirm_rent_application(self):
        rent_id = RentApplication.objects.get(description='101112')
        response = self.client.post('/api/v1/rent-application/' + str(rent_id) + '/return/confirm/')

        rent_equipment = rent_id.equipment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rent_equipment.status, 'AVA')
        self.assertEqual(rent_equipment.borrower, None)
        self.assertEqual(RentApplication.objects.get(description='101112').applying, False)
