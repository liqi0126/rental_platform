from application.release_application.models import ReleaseApplication
from application.release_application.serializers import ReleaseApplicationSerializer
from equipment.models import Equipment
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets
from rest_framework.decorators import action

from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from django.core.mail import send_mail

import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class ReleaseApplicationViewSet(viewsets.ModelViewSet):
    queryset = ReleaseApplication.objects.all()
    serializer_class = ReleaseApplicationSerializer

    filter_fields = '__all__'
    search_fields = ['description', 'comments']
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        while True:
            equipment_id = self.request.POST.get('equipment', '')
            print(equipment_id)
            try:
                equipment = Equipment.objects.get(id=equipment_id)
            except:
                print(1)
                raise NotFound(detail=None, code=None)

            origin_eq_status = equipment.status
            if origin_eq_status != Equipment.Status.UNRELEASED:
                raise ValidationError(detail='equipment has been released', code=status.HTTP_400_BAD_REQUEST)

            if not Equipment.objects.filter(id=equipment_id, status=origin_eq_status).update(status=Equipment.Status.UNAPPROVED):
                continue
            break

        logger.info('create a release application with equipment: { id: ' + str(equipment.id) + ', name: ' + str(
            equipment.name) + '}')
        serializer.save(owner=equipment.owner)

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            logger.info('update a release application(through put): ' + str(serializer.validated_data))
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info('update a release application(through patch): ' + str(request.data))
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        logger.info('delete a release application: ' + str(instance))
        instance.delete()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        comments = request.POST.get('comments', '')

        with transaction.atomic():
            while True:
                try:
                    release_application = ReleaseApplication.objects.get(pk=pk)
                except ReleaseApplication.DoesNotExist:
                    return Response({'error': 'release application not found'}, status=status.HTTP_404_NOT_FOUND)

                origin_application_status = release_application.status

                if origin_application_status != ReleaseApplication.Status.UNAPPROVED:
                    return Response({'error': 'application has been accepted or rejected'}, status=status.HTTP_400_BAD_REQUEST)

                release_equipment = Equipment.objects.get(id=release_application.equipment.id)
                origin_eq_status = release_equipment.status
                origin_eq_is_released = release_equipment.is_released

                if origin_eq_status != Equipment.Status.UNAPPROVED:
                    return Response({'error': 'the equipment is not in UNAPPROVED status'}, status=status.HTTP_400_BAD_REQUEST)

                if not Equipment.objects\
                        .filter(id=release_equipment.id, status=origin_eq_status, is_released=origin_eq_is_released)\
                        .update(status=Equipment.Status.AVAILABLE, is_released=True):
                    continue

                if not ReleaseApplication.objects.filter(pk=pk, status=origin_application_status) \
                        .update(comments=comments, status=ReleaseApplication.Status.ACCEPTED):
                    continue
                break

        serializer = ReleaseApplicationSerializer(release_application)
        logger.info('change the status of the release application: { id: ' + str(release_application.id)
                    + ' } to accepted and change the status of the equipment to available')
        equipment = Equipment.objects.get(id=release_application.equipment.id)
        email_address = equipment.owner.email
        send_mail('[rental_platform.com] Please Check Your Application Status Updates'
                  , 'Hello from rental_platform.com!\n\n'
                    'You\'re receiving this e-mail because your RELEASE application for certain equipment: \n\n'
                    'name: ' + equipment.name +
                    '\nowner: ' + equipment.owner.first_name + ' ' + equipment.owner.last_name +
                    '\ndescription: ' + equipment.description +
                    '\nphone: ' + equipment.phone +
                    '\nemail: ' + equipment.email +
                    '\naddress: ' + equipment.address + '\n\n'
                    'has been APPROVED by the '
                    'administrator with comments as below: \n\n' + '"' + comments + '"' +
                  '\n\nThank you from rental_platform.com!\n'
                  'rental_platform.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk):
        comments = request.POST.get('comments', '')

        with transaction.atomic():
            while True:
                try:
                    release_application = ReleaseApplication.objects.get(pk=pk)
                except ReleaseApplication.DoesNotExist:
                    return Response({'detail': 'release application not found'}, status=status.HTTP_404_NOT_FOUND)

                origin_application_status = release_application.status

                if origin_application_status != ReleaseApplication.Status.UNAPPROVED:
                    return Response({'detail': 'application has been accepted or rejected'}, status=status.HTTP_400_BAD_REQUEST)

                release_equipment = Equipment.objects.get(id=release_application.equipment.id)
                origin_eq_status = release_equipment.status
                origin_eq_is_released = release_equipment.is_released

                if origin_eq_status != Equipment.Status.UNAPPROVED:
                    return Response({'error': 'the equipment is not in UNAPPROVED status'}, status=status.HTTP_400_BAD_REQUEST)

                if not Equipment.objects\
                        .filter(id=release_application.equipment.id, status=origin_eq_status, is_released=origin_eq_is_released)\
                        .update(status=Equipment.Status.UNRELEASED, is_released=False):
                    continue
                if not ReleaseApplication.objects. \
                        filter(pk=pk, status=origin_application_status). \
                        update(comments=comments, status=ReleaseApplication.Status.REJECTED):
                    continue
                break

        logger.info('change the status of the release application: { id: ' + str(release_application.id)
                    + ' } to rejected')
        email_address = release_equipment.owner.email
        send_mail('[rental_platform.com] Please Check Your Application Status Updates'
                  , 'Hello from rental_platform.com!\n\n'
                    'You\'re receiving this e-mail because your RELEASE application for certain equipment: \n\n'
                    'name: ' + release_equipment.name +
                    '\nowner: ' + release_equipment.owner.first_name + ' ' + release_equipment.owner.last_name +
                    '\ndescription: ' + release_equipment.description +
                    '\nphone: ' + release_equipment.phone +
                    '\nemail: ' + release_equipment.email +
                    '\naddress: ' + release_equipment.address + '\n\n'
                    'has been REJECTED by the '
                    'administrator with comments as below: \n\n' + '"' + comments + '"' +
                  '\n\nThank you from rental_platform.com!\n'
                  'rental_platform.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)

        serializer = ReleaseApplicationSerializer(release_application)
        return Response(serializer.data)