from django.http import JsonResponse
from user.models import User
from user.serializers import UserSerializer

from rest_framework.views import APIView


from django.http import QueryDict, HttpResponse


from rest_framework import generics
# Create your views here.


# high level API
class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_fields = ['email']
    search_fields = ['email']
    ordering_fields = '__all__'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_fields = ['']

