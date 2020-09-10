from user.models import User
from user.serializers import UserSerializer
from rest_framework import viewsets

import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_fields = '__all__'
    search_fields = ['first_name', 'last_name', 'address']
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        logger.info('create a new user: { last_name: ' + str(serializer.validated_data.get('last_name'))
                    + ', first_name: ' + str(serializer.validated_data.get('first_name')) + ' }')
        serializer.save()

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            logger.info('update a user(through put): { last_name: ' + str(serializer.validated_data.get('last_name'))
                        + ', first_name: ' + str(serializer.validated_data.get('first_name')) + ' }')
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info('update a user(through patch): { last_name: ' + str(request.data.get('last_name'))
                    + ', first_name: ' + str(request.data.get('first_name')) + ' }')
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        logger.info('delete a user: ' + str(instance))
        instance.delete()
