from rest_framework.test import APITestCase
from rest_framework import status
from .models import RenterApplication
from user.models import User


# Create your tests here.
class RenterApplicationTestCase(APITestCase):
    def setUp(self):
        user_one = User.objects.create(email='123@qq.com', password='123123', address='123123', phone='15801266030')
        user_two = User.objects.create(email='456@qq.com', password='456456', address='456456', phone='18012357727')
        RenterApplication.objects.create(applicant=user_one, description='789789')
        RenterApplication.objects.create(applicant=user_two, description='456456')

    def test_approve_renter_application(self):
        data = {
            'comments': 'good job'
        }

        renter_id = RenterApplication.objects.get(description='789789')
        response = self.client.post('/api/v1/renter-application/' + str(renter_id) + '/approve/', data)

        renter = renter_id.applicant
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'ACC')
        self.assertEqual(renter.is_renter, True)

    def test_reject_renter_application(self):
        data = {
            'comments': 'too bad'
        }

        renter_id = RenterApplication.objects.get(description='456456')
        response = self.client.post('/api/v1/renter-application/' + str(renter_id) + '/reject/', data)

        renter = renter_id.applicant
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('status'), 'REJ')
        self.assertEqual(renter.is_renter, False)
