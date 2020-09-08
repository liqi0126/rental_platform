from django.shortcuts import render
from django.http import JsonResponse
from application.release_application.models import ReleaseApplication
from application.release_application.serializers import ReleaseApplicationSerializer
from equipment.models import Equipment
from user.models import User
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response


class ReleaseApplicationList(APIView):
    def post(self, request, format=None):
        equipment_name = request.POST.get('equipment', '')
        description = request.POST.get('description', '')

        try:
            equipment = Equipment.objects.get(name=equipment_name)
        except:
            return JsonResponse({'error': 'no such an equipment'})

        owner = equipment.owner

        release_application = ReleaseApplication(equipment=equipment, owner=owner, description=description)
        release_application.save()
        serializer = ReleaseApplicationSerializer(release_application)
        return Response(serializer.data)

    def get(self, request, format=None):
        release_application_list = ReleaseApplication.objects.all()
        serializer = ReleaseApplicationSerializer(release_application_list, many=True)
        return Response(serializer.data)


class ReleaseApplicationDetail(APIView):
    def get(self, request, pk, format=None):
        release_application = ReleaseApplication.objects.filter(id=pk)
        serializer = ReleaseApplicationSerializer(release_application.first())
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        try:
            ReleaseApplication.objects.filter(id=pk).delete()
            return JsonResponse('ok', safe=False)
        except:
            return JsonResponse('error', safe=False)


class ReleaseApplicationAccept(APIView):
    def post(self, request, pk, format=None):
        release_application = ReleaseApplication.objects.filter(id=pk)
        release_application.update(status='ACC')
        serializer = ReleaseApplicationSerializer(release_application.first())
        return Response(serializer.data)


class ReleaseApplicationReject(APIView):
    def post(self, request, pk, format=None):
        release_application = ReleaseApplication.objects.filter(id=pk)
        release_application.update(status='REJ')
        serializer = ReleaseApplicationSerializer(release_application.first())
        return Response(serializer.data)