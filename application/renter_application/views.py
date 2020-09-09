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
import json


class RenterApplicationList(generics.ListCreateAPIView):
    queryset = RenterApplication.objects.all()
    serializer_class = RenterApplicationSerializer

    filter_fields = '__all__'
    search_fields = ['description', 'comments']
    ordering_fields = '__all__'

    # def perform_create(self, serializer):
    #     applicant_id = self.request.POST.get('applicant', '')
    #     description = self.request.POST.get('description', '')
    #
    #     try:
    #         applicant = User.objects.get(id=applicant_id)
    #     except:
    #         return JsonResponse({'error': 'no such a user'})
    #
    #     serializer.save(applicant=applicant, description=description)

# Create your views here.
# class RenterApplicationList(APIView):
#
#     filter_fields = ['status']
#
#     def post(self, request, format=None):
#         applicant_id = request.POST.get('applicant', '')
#         description = request.POST.get('description', '')
#
#         try:
#             applicant = User.objects.get(id=applicant_id)
#         except:
#             return Response({'error': 'no such a user'}, status=400)
#
#         renter_application = RenterApplication(applicant=applicant, description=description)
#         renter_application.save()
#         serializer = RenterApplicationSerializer(renter_application)
#         return Response(serializer.data)
#
#     def get(self, request, format=None):
#         page = request.POST.get('page', 1)
#         size = request.POST.get('size', 5)
#         user_id = request.POST.get('user_id', 0)
#         is_asc = request.POST.get('is_asc', 'True')
#         # application_status = request.POST.get('application_status', '')
#         renter_application_list = RenterApplication.objects.all()
#         if user_id != 0:
#             try:
#                 user = User.objects.get(id=user_id)
#             except:
#                 return Response({'error': 'no such a user'}, status=400)
#             renter_application_list = renter_application_list.filter(applicant=user)
#         if is_asc == 'True':
#             renter_application_list = renter_application_list.order_by('id')
#         elif is_asc == 'False':
#             renter_application_list = renter_application_list.order_by('-id')
#         else:
#             Response({'error': 'no such a sort_order'}, status=400)
#         # if application_status != '':
#         #     if application_status != 'UNA' and application_status != 'ACC' and application_status != 'REJ':
#         #         return Response({'error': 'no such a status'}, status=400)
#         #     else:
#         #         renter_application_list = renter_application_list.filter(status=application_status)
#         renter_application_list = renter_application_list[(page-1)*size:page*size]
#         serializer = RenterApplicationSerializer(renter_application_list, many=True)
#         return Response(serializer.data)


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


class RenterApplicationOfUser(APIView):
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(id=pk)
        except:
            return Response({'error': 'no such a user'}, status=400)
        renter_application = RenterApplication.objects.filter(applicant=user)
        serializer = RenterApplicationSerializer(renter_application, many=True)
        return Response(serializer.data)
