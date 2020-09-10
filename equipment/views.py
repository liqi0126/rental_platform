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
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()