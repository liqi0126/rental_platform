from rest_framework.test import APITestCase
from rest_framework import status
from .models import Equipment
from user.models import User


# Create your tests here.
class EquipmentTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(email='123@qq.com', password='123123', address='123123', phone='15801266030')
        Equipment.objects.create(email='123@qq.com', phone='18012357727', address='北京市海淀区', name='光谱仪'
                                 , description='1w23', owner=user, status='AVA', is_released=True)

    def test_withdraw_equipment(self):
        response = self.client.post('/api/v1/equipment/' + str(Equipment.objects.get(name='光谱仪').id) + '/withdraw/')
        equipment_withdraw = Equipment.objects.get(name='光谱仪')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(equipment_withdraw.status, 'UNR')
        self.assertEqual(equipment_withdraw.is_released, False)
