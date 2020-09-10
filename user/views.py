from user.models import User
from user.serializers import UserSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_fields = '__all__'
    search_fields = ['first_name', 'last_name', 'address']
    ordering_fields = '__all__'