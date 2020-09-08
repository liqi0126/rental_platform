from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer


from rest_framework import generics

# Create your views here.


# high level API
class EquipmentList(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class EquipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
