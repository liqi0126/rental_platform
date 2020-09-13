from rest_framework.test import APITestCase
from rest_framework import status
from .models import Message
from user.models import User
from rest_framework.authtoken.models import Token


# Create your tests here.
class MessageTestCase(APITestCase):
    def setUp(self):
        User.objects.create(email='1@qq.com', password='123123', address='12123', phone='15801266030', is_staff=True)
        person_one = User.objects.create(email='123@qq.com', password='123123', address='123123', phone='15801266030'
                                         , first_name='三', last_name='张')
        person_two = User.objects.create(email='456@qq.com', password='456456', address='456456', phone='18012357727'
                                         , first_name='四', last_name='李')
        person_three = User.objects.create(email='789@qq.com', password='789789', address='789789', phone='15052116911'
                                           , first_name='五', last_name='王')
        Message.objects.create(sender=person_one, receiver=person_three, text="hape1")
        Message.objects.create(sender=person_two, receiver=person_one, text="hape2")
        Message.objects.create(sender=person_one, receiver=person_two, text="hape3")
        Message.objects.create(sender=person_three, receiver=person_two, text="hape4")
        Message.objects.create(sender=person_two, receiver=person_one, text="hape5")
        Message.objects.create(sender=person_one, receiver=person_three, text="hape6")
        Message.objects.create(sender=person_two, receiver=person_three, text="hape7")
        Message.objects.create(sender=person_three, receiver=person_two, text="hape8")
        Message.objects.create(sender=person_one, receiver=person_two, text="hape9")

    def test_chats_message(self):
        for user in User.objects.all():
            Token.objects.create(user=user)
        token = Token.objects.get(user=User.objects.get(email='1@qq.com'))
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        id_one = User.objects.get(email='123@qq.com').id
        id_two = User.objects.get(email='456@qq.com').id
        response = self.client.get('/api/v1/message/chats/?id_one=' + str(id_one) + '&id_two=' + str(id_two))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
