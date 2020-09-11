from application.release_application.models import ReleaseApplication
from application.release_application.serializers import ReleaseApplicationSerializer
from equipment.models import Equipment
from user.models import User
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import action

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
        equipment_id = self.request.POST.get('equipment', '')
        try:
            equipment = Equipment.objects.get(id=equipment_id)
        except:
            return Response({'error': 'no such an equipment'}, status=400)
        release_equipment = Equipment.objects.filter(id=equipment.id)
        release_equipment.update(status='UNA')
        logger.info('create a release application with equipment: { id: ' + str(equipment.id) + ', name: ' + str(
            equipment.name) + '}')
        serializer.save(owner=equipment.owner)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        release_application = ReleaseApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        release_application.update(comments=comments)
        release_application.update(status='ACC')
        release_equipment = Equipment.objects.filter(id=release_application.first().equipment.id)
        release_equipment.update(status='AVA')
        release_equipment.update(is_released=True)
        serializer = ReleaseApplicationSerializer(release_application.first())
        logger.info('change the status of the release application: { id: ' + str(release_application.first().id)
                    + ' } to accepted and change the status of the equipment to available')
        equipment = Equipment.objects.get(id=release_application.first().equipment.id)
        email_address = equipment.owner.email
        send_mail('[example.com] Please Check Your Application Status Updates'
                  , 'Hello from example.com!\n\n'
                    'You\'re receiving this e-mail because your RELEASE application for certain equipment: \n\n'
                    'name: ' + equipment.name +
                    '\nowner: ' + equipment.owner.first_name + ' ' + equipment.owner.last_name +
                    '\ndescription: ' + equipment.description +
                    '\nphone: ' + equipment.phone +
                    '\nemail: ' + equipment.email +
                    '\naddress: ' + equipment.address + '\n\n'
                    'has been APPROVED by the '
                    'administrator with comments as below: \n\n' + '"' + comments + '"' +
                  '\n\nThank you from example.com!\n'
                  'example.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk):
        release_application = ReleaseApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        release_application.update(comments=comments)
        release_application.update(status='REJ')
        serializer = ReleaseApplicationSerializer(release_application.first())
        logger.info('change the status of the release application: { id: ' + str(release_application.first().id)
                    + ' } to rejected')
        equipment = Equipment.objects.get(id=release_application.first().equipment.id)
        Equipment.objects.filter(id=release_application.first().equipment.id).update(is_released=False)
        email_address = equipment.owner.email
        send_mail('[example.com] Please Check Your Application Status Updates'
                  , 'Hello from example.com!\n\n'
                    'You\'re receiving this e-mail because your RELEASE application for certain equipment: \n\n'
                    'name: ' + equipment.name +
                    '\nowner: ' + equipment.owner.first_name + ' ' + equipment.owner.last_name +
                    '\ndescription: ' + equipment.description +
                    '\nphone: ' + equipment.phone +
                    '\nemail: ' + equipment.email +
                    '\naddress: ' + equipment.address + '\n\n'
                    'has been REJECTED by the '
                    'administrator with comments as below: \n\n' + '"' + comments + '"' +
                  '\n\nThank you from example.com!\n'
                  'example.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)
        return Response(serializer.data)

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
