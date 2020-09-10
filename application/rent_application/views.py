from application.rent_application.models import RentApplication
from application.rent_application.serializers import RentApplicationSerializer
from equipment.models import Equipment
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import action

from django.core.mail import send_mail

import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class RentApplicationViewSet(viewsets.ModelViewSet):
    queryset = RentApplication.objects.all()
    serializer_class = RentApplicationSerializer

    def perform_create(self, serializer):
        equipment_id = self.request.POST.get('equipment', '')
        try:
            equipment = Equipment.objects.get(id=equipment_id)
        except:
            return Response({'error': 'no such an equipment'}, status=400)
        logger.info('create a rent application with equipment: { id: ' + str(equipment.id) + ', name: ' + str(
            equipment.name) + '}')
        serializer.save(renter=equipment.owner)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        rent_application = RentApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        rent_equipment = Equipment.objects.filter(id=rent_application.first().equipment.id)
        rent_equipment.update(status='REN')
        rent_equipment.update(borrower=RentApplication.objects.get(id=pk).borrower)
        rent_application.update(comments=comments)
        rent_application.update(status='ACC')
        rent_application.update(applying=True)
        serializer = RentApplicationSerializer(rent_application.first())
        logger.info('change the status of the rent application: { id: ' + str(rent_application.first().id)
                    + ' } to accepted and change the status of the equipment to rented')
        email_address = RentApplication.objects.get(id=pk).renter
        equipment = Equipment.objects.get(id=rent_application.first().equipment.id)
        send_mail('[example.com] Please Check Your Application Status Updates'
                  , 'Hello from example.com!\n\n'
                    'You\'re receiving this e-mail because your RENT application for certain equipment: \n\n'
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
        rent_application = RentApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        rent_application.update(comments=comments)
        rent_application.update(status='REJ')
        rent_application.update(applying=False)
        serializer = RentApplicationSerializer(rent_application.first())
        logger.info('change the status of the rent application: { id: ' + str(rent_application.first().id)
                    + ' } to rejected')
        email_address = RentApplication.objects.get(id=pk).renter
        equipment = Equipment.objects.get(id=rent_application.first().equipment.id)
        Equipment.objects.filter(id=rent_application.first().equipment.id).update(borrower=None)
        send_mail('[example.com] Please Check Your Application Status Updates'
                  , 'Hello from example.com!\n\n'
                    'You\'re receiving this e-mail because your RENT application for certain equipment: \n\n'
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

    @action(detail=True, methods=['post'], url_path='return')
    def return_post(self, request, pk):
        if RentApplication.objects.get(id=pk).status == 'ACC':
            rent_application = RentApplication.objects.filter(id=pk)
            user_comments = request.POST.get('user_comments', '')
            rent_application.update(user_comments=user_comments)
            # rent_application.update(status='RET')
            rent_application.update(applying=False)
            rent_equipment = Equipment.objects.filter(id=rent_application.first().equipment.id)
            rent_equipment.update(status='RET')
            rent_equipment.update(borrower=None)
            serializer = RentApplicationSerializer(rent_application.first())
            logger.info('change the status of the rent application: { id: ' + str(rent_application.first().id)
                        + ' } to returned and change the status of the equipment to returned')
        else:
            return Response({'error': 'cannot return before rent'}, status=400)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='return/confirm')
    def return_confirm_post(self, request, pk):
        rent_application = RentApplication.objects.filter(id=pk)
        if Equipment.objects.get(id=rent_application.first().equipment.id).status == 'RET':
            rent_application = RentApplication.objects.filter(id=pk)
            release_equipment = Equipment.objects.filter(id=rent_application.first().equipment.id)
            release_equipment.update(status='AVA')
            release_equipment.update(borrower=None)
            serializer = RentApplicationSerializer(rent_application.first())
            logger.info('keep the status of the rent application: { id: ' + str(rent_application.first().id)
                        + ' } as returned and change the status of the equipment to available')
        else:
            return Response({'error': 'cannot confirm return before return'}, status=400)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            logger.info('update a rent application(through put): ' + str(serializer.validated_data))
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info('update a rent application(through patch): ' + str(request.data))
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        logger.info('delete a rent application: ' + str(instance))
        instance.delete()

    filter_fields = '__all__'
    search_fields = ['description', 'comments', 'user_comments']
    ordering_fields = '__all__'
