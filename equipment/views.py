from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer

from rest_framework import viewsets

# Create your views here.


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    filter_fields = '__all__'
    search_fields = ['name', 'address', 'description']
    ordering_fields = '__all__'
