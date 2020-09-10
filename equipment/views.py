from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer

from rest_framework import viewsets

from django.http import HttpResponse

# Create your views here.


import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    filter_fields = '__all__'
    search_fields = ['name', 'address', 'description']
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        logger.info('create a new equipment: { name: ' + str(serializer.validated_data.get('name')) + ' }')
        serializer.save()

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            logger.info('update an equipment(through put): { name: ' + str(serializer.validated_data.get('name'))
                        + ' }')
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info('update an equipment(through patch): ' + str(request.data))
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        logger.info('delete an equipment: { name: ' + str(instance) + ' }')
        instance.delete()
