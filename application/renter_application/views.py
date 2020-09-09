from django.shortcuts import render
from django.http import JsonResponse
from application.renter_application.models import RenterApplication
from application.renter_application.serializers import RenterApplicationSerializer
from equipment.models import Equipment
from user.models import User
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics


# Create your views here.
class RenterApplicationList(APIView):
    def post(self, request, format=None):
        applicant_id = request.POST.get('applicant', '')
        description = request.POST.get('description', '')

        try:
            applicant = User.objects.get(id=applicant_id)
        except:
            return JsonResponse({'error': 'no such a user'})

        renter_application = RenterApplication(applicant=applicant, description=description)
        renter_application.save()
        serializer = RenterApplicationSerializer(renter_application)
        return Response(serializer.data)

    def get(self, request, format=None):
        renter_application_list = RenterApplication.objects.all()
        serializer = RenterApplicationSerializer(renter_application_list, many=True)
        return Response(serializer.data)


# high level API
class RenterApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RenterApplication.objects.all()
    serializer_class = RenterApplicationSerializer


# class RenterApplicationDetail(APIView):
#     def get(self, request, pk, format=None):
#         renter_application = RenterApplication.objects.filter(id=pk)
#         serializer = RenterApplicationSerializer(renter_application.first())
#         return Response(serializer.data)
#
#     def delete(self, request, pk, format=None):
#         try:
#             RenterApplication.objects.filter(id=pk).delete()
#             return JsonResponse('ok', safe=False)
#         except:
#             return JsonResponse('error', safe=False)


class RenterApplicationAccept(APIView):
    def post(self, request, pk, format=None):
        renter_application = RenterApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        renter_application.update(comments=comments)
        renter_application.update(status='ACC')
        serializer = RenterApplicationSerializer(renter_application.first())
        return Response(serializer.data)


class RenterApplicationReject(APIView):
    def post(self, request, pk, format=None):
        renter_application = RenterApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        renter_application.update(comments=comments)
        renter_application.update(status='REJ')
        serializer = RenterApplicationSerializer(renter_application.first())
        return Response(serializer.data)
