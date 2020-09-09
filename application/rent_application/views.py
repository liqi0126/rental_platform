from django.shortcuts import render
from django.http import JsonResponse
from application.rent_application.models import RentApplication
from application.rent_application.serializers import RentApplicationSerializer
from equipment.models import Equipment
from user.models import User
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response


class RentApplicationList(APIView):
    def post(self, request, format=None):
        equipment_id = request.POST.get('equipment', '')
        hirer_id = request.POST.get('hirer', '')
        description = request.POST.get('description', '')
        lease_term_begin = request.POST.get('lease_term_begin', '')
        lease_term_end = request.POST.get('lease_term_end', '')

        try:
            hirer = User.objects.get(id=hirer_id)
        except:
            return JsonResponse({'error': 'no such a user'})

        try:
            equipment = Equipment.objects.get(id=equipment_id)
        except:
            return JsonResponse({'error': 'no such an equipment'})

        renter = equipment.owner

        rent_application = RentApplication(equipment=equipment, renter=renter, hirer=hirer, description=description
                                           , lease_term_begin=lease_term_begin, lease_term_end=lease_term_end)
        rent_application.save()
        serializer = RentApplicationSerializer(rent_application)
        return Response(serializer.data)

    def get(self, request, format=None):
        rent_application_list = RentApplication.objects.all()
        serializer = RentApplicationSerializer(rent_application_list, many=True)
        return Response(serializer.data)


class RentApplicationDetail(APIView):
    def get(self, request, pk, format=None):
        rent_application = RentApplication.objects.filter(id=pk)
        serializer = RentApplicationSerializer(rent_application.first())
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        try:
            RentApplication.objects.filter(id=pk).delete()
            return JsonResponse('ok', safe=False)
        except:
            return JsonResponse('error', safe=False)


class RentApplicationAccept(APIView):
    def post(self, request, pk, format=None):
        rent_application = RentApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        rent_application.update(comments=comments)
        rent_application.update(status='ACC')
        rent_application.update(applying=True)
        serializer = RentApplicationSerializer(rent_application.first())
        return Response(serializer.data)


class RentApplicationReject(APIView):
    def post(self, request, pk, format=None):
        rent_application = RentApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        rent_application.update(comments=comments)
        rent_application.update(status='REJ')
        rent_application.update(applying=False)
        serializer = RentApplicationSerializer(rent_application.first())
        return Response(serializer.data)


class RentApplicationReturn(APIView):
    def post(self, request, pk, format=None):
        rent_application = RentApplication.objects.filter(id=pk)
        user_comments = request.POST.get('user_comments', '')
        rent_application.update(user_comments=user_comments)
        rent_application.update(status='RET')
        rent_application.update(applying=False)
        serializer = RentApplicationSerializer(rent_application.first())
        return Response(serializer.data)
