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
        equipment_id = request.POST.get('equipment', '')
        description = request.POST.get('description', '')

        try:
            equipment = Equipment.objects.get(id=equipment_id)
        except:
            return JsonResponse({'error': 'no such an equipment'})

        owner = equipment.owner
        equipment.status = 'UNA'

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
        comments = request.POST.get('comments', '')
        release_application.update(comments=comments)
        release_application.update(status='ACC')
        release_equipment = Equipment.objects.filter(id=release_application.first().equipment.id)
        release_equipment.update(status='AVA')
        serializer = ReleaseApplicationSerializer(release_application.first())
        return Response(serializer.data)


class ReleaseApplicationReject(APIView):
    def post(self, request, pk, format=None):
        release_application = ReleaseApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        release_application.update(comments=comments)
        release_application.update(status='REJ')
        serializer = ReleaseApplicationSerializer(release_application.first())
        return Response(serializer.data)