from user.models import User
from user.serializers import UserSerializer
from rest_framework import viewsets


from rest_framework import generics
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_fields = '__all__'
    search_fields = ['first_name', 'last_name', 'address']
    ordering_fields = '__all__'


# high level API
# class UsersList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     filter_fields = '__all__'
#     search_fields = ['first_name', 'last_name', 'address']
#     ordering_fields = '__all__'
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



