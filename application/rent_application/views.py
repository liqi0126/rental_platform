from application.rent_application.models import RentApplication
from application.rent_application.serializers import RentApplicationSerializer
from equipment.models import Equipment
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import action

from django.core.mail import send_mail
import pytz
import datetime

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
        if Equipment.objects.get(id=rent_application.first().equipment.id).status != 'REN':
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
            email_address = RentApplication.objects.get(id=pk).borrower
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
        else:
            return Response({'error': 'the equipment has already been rented'}, status=400)
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
        email_address = RentApplication.objects.get(id=pk).borrower
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
            # rent_application.update(applying=False)
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
            rent_equipment = Equipment.objects.filter(id=rent_application.first().equipment.id)
            rent_equipment.update(status='AVA')
            rent_equipment.update(borrower=None)
            rent_application.update(applying=False)
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


def expire_reminder():
    utc_tz = pytz.timezone('UTC')
    rent_applications = RentApplication.objects.filter(applying=True)
    for rent_application in rent_applications:
        lease_term_end = rent_application.lease_term_end
        current_time = datetime.datetime.now(tz=utc_tz)
        seconds_delta = (current_time - lease_term_end).total_seconds()

        if seconds_delta > 60 * 60 * 24:
            return

        if seconds_delta < 0:
            expire_message = 'has expired!'
        elif seconds_delta < 60 * 60:
            expire_message = 'is going to expire less than 1 hour!'
        else:
            expire_message = 'is going to expire less than 1 day!'

        send_mail('[example.com] Your Rented Equipment Is Going To Expire'
                  , 'Hello from example.com!\n\n'
                    'You\'re receiving this e-mail because your rented equipment [' + rent_application.equipment.name + '] '
                  + expire_message + ' Please return it timely!' +
                  '\n\nThank you from example.com!\n'
                  'example.com'
                  , '624275030@qq.com', [rent_application.borrower.email], fail_silently=False)



from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from django_apscheduler.jobstores import DjangoJobStore, register_job

try:
    # 实例化调度器

    scheduler = BackgroundScheduler(jobstores={
        'default': MemoryJobStore()
    })

    # 调度器使用DjangoJobStore()
    # scheduler.add_jobstore(DjangoJobStore(), "default")
    # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次

    @register_job(scheduler, 'interval', seconds=1, id='expire_reminder')
    def expire_reminder():
        utc_tz = pytz.timezone('UTC')
        rent_applications = RentApplication.objects.filter(applying=True)
        for rent_application in rent_applications:
            lease_term_end = rent_application.lease_term_end
            current_time = datetime.datetime.now(tz=utc_tz)
            seconds_delta = (lease_term_end - current_time).total_seconds()

            if seconds_delta > 60 * 60 * 24:
                return

            if seconds_delta < 0:
                if rent_application.expired_reminded:
                    return
                expire_message = 'has expired!'
                rent_application.expired_reminded = True
                rent_application.save()
            elif seconds_delta < 60 * 60:
                if rent_application.expire_before_hour_reminded:
                    return
                expire_message = 'is going to expire less than 1 hour!'
                rent_application.expire_before_hour_reminded = True
                rent_application.save()
            else:
                if rent_application.expire_before_day_reminded:
                    return
                expire_message = 'is going to expire less than 1 day!'
                rent_application.expire_before_day_reminded = True
                rent_application.save()

            send_mail('[example.com] Your Rented Equipment Is Going To Expire'
                      , 'Hello from example.com!\n\n'
                        'You\'re receiving this e-mail because your rented equipment [' + rent_application.equipment.name + '] '
                      + expire_message + ' Please return it timely!' +
                      '\n\nThank you from example.com!\n'
                      'example.com'
                      , '624275030@qq.com', [rent_application.borrower.email], fail_silently=False)


    # 调度器开始
    scheduler.start()
except:
    scheduler.shutdown()
