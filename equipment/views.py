from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed

from equipment.models import Equipment
from user.models import User
from equipment.serializers import EquipmentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class EquipmentsBatch(APIView):

    def post(self, request, format=None):
        if request.method == 'POST':
            name = request.POST.get('name', '')
            address = request.POST.get('address', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            description = request.POST.get('description', '')

            owner_name = request.POST.get('owner', '')
            try:
                owner = User.objects.get(username=owner_name)
            except:
                return JsonResponse({'error': 'no such a user'})

            equipment = Equipment(name=name, address=address, email=email, phone=phone, description=description,
                                  owner=owner)

            equipment.save()

            return JsonResponse({'equipment': name})

    def get(self, request, format=None):
        equipment_list = Equipment.objects.all()
        serializer = EquipmentSerializer(equipment_list, many=True)
        return Response(serializer.data)


class EquipmentSingle(APIView):

    def get(self, request, equipment_id, format=None):
        equipment = Equipment.objects.filter(id=equipment_id)
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

    def delete(self, request, equipment_id, format=None):
        try:
            Equipment.objects.filter(id=equipment_id).delete()
            return JsonResponse('ok', safe=False)
        except:
            return JsonResponse('error', safe=False)
