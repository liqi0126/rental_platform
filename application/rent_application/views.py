from application.rent_application.models import RentApplication
from application.rent_application.serializers import RentApplicationSerializer
from equipment.models import Equipment
from user.models import User
from rest_framework.response import Response

from rest_framework import viewsets, status
from rest_framework.decorators import action

from django.db import transaction
from rest_framework.exceptions import ValidationError
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
        borrower_id = self.request.POST.get('borrower', '')
        equipment_id = self.request.POST.get('equipment', '')
        try:
            borrower = User.objects.get(id=borrower_id)
        except User.DoesNotExist:
            raise ValidationError(detail='no such an user', code=404)
        if not borrower.is_renter:
            raise ValidationError(detail='borrower is not a renter', code=status.HTTP_400_BAD_REQUEST)
        try:
            equipment = Equipment.objects.get(id=equipment_id)
        except Equipment.DoesNotExist:
            raise ValidationError(detail='no such an equipment', code=404)

        logger.info('create a rent application with equipment: { id: ' + str(equipment.id) + ', name: ' + str(
            equipment.name) + '}')
        email_address = equipment.owner.email
        equipment_borrower = User.objects.get(id=self.request.data.get('borrower'))
        send_mail('[rental_platform.com] Please Check Your Equipment\'s Newly Received Rent Application'
                  , 'Hello from rental_platform.com!\n\n'
                    'You\'re receiving this e-mail because your equipment: \n\n'
                    'name: ' + equipment.name +
                  '\nowner: ' + equipment.owner.first_name + ' ' + equipment.owner.last_name +
                  '\ndescription: ' + equipment.description +
                  '\nphone: ' + equipment.phone +
                  '\nemail: ' + equipment.email +
                  '\naddress: ' + equipment.address + '\n\n'
                                                      'has received a new RENT application from: \n\n'
                  + '"' + equipment_borrower.first_name + ' ' + equipment_borrower.last_name + '"' +
                  '\n\nPlease deal with the application on time!'
                  '\nThank you from rental_platform.com!\n'
                  'rental_platform.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)
        serializer.save(renter=equipment.owner)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        comments = request.POST.get('comments', '')
        with transaction.atomic():
            while True:
                try:
                    rent_application = RentApplication.objects.get(pk=pk)
                except RentApplication.DoesNotExist:
                    return Response({'detail': 'rent application not found'}, status=status.HTTP_404_NOT_FOUND)

                if not rent_application.borrower.is_renter:
                    raise ValidationError(detail='borrower is not a renter', code=status.HTTP_400_BAD_REQUEST)

                origin_application_status = rent_application.status

                if origin_application_status != RentApplication.Status.UNAPPROVED:
                    return Response({'detail': 'rent application has been approved or rejected'}, status=status.HTTP_400_BAD_REQUEST)

                equipment = Equipment.objects.get(id=rent_application.equipment.id)
                origin_eq_status = equipment.status

                if origin_eq_status != Equipment.Status.AVAILABLE:
                    return Response({'detail': 'equipment is not available'}, status=status.HTTP_400_BAD_REQUEST)

                if not Equipment.objects \
                        .filter(id=rent_application.equipment.id, status=origin_eq_status) \
                        .update(status=Equipment.Status.RENTED, borrower=rent_application.borrower):
                    continue

                if not RentApplication.objects.filter(pk=pk, status=origin_application_status) \
                        .update(status=RentApplication.Status.ACCEPTED, applying=True, comments=comments):
                    continue
                break

        serializer = RentApplicationSerializer(rent_application)
        logger.info('change the status of the rent application: { id: ' + str(rent_application.id)
                    + ' } to accepted and change the status of the equipment to rented')
        email_address = RentApplication.objects.get(id=pk).borrower.email
        equipment = Equipment.objects.get(id=rent_application.equipment.id)
        send_mail('[rental_platform.com] Please Check Your Application Status Updates'
                  , 'Hello from rental_platform.com!\n\n'
                    'You\'re receiving this e-mail because your RENT application for certain equipment: \n\n'
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
                    rent_application = RentApplication.objects.get(pk=pk)
                except RentApplication.DoesNotExist:
                    return Response({'detail': 'rent application not found'}, status=status.HTTP_404_NOT_FOUND)

                if not rent_application.borrower.is_renter:
                    raise ValidationError(detail='borrower is not a renter', code=status.HTTP_400_BAD_REQUEST)

                origin_application_status = rent_application.status

                if origin_application_status != RentApplication.Status.UNAPPROVED:
                    return Response({'detail': 'rent application has been approved or rejected'}, status=status.HTTP_400_BAD_REQUEST)

                equipment = Equipment.objects.get(id=rent_application.equipment.id)
                origin_eq_status = equipment.status

                if origin_eq_status != Equipment.Status.AVAILABLE:
                    return Response({'detail': 'equipment is not available'}, status=status.HTTP_400_BAD_REQUEST)

                if not Equipment.objects.filter(id=rent_application.equipment.id, status=origin_eq_status).update(borrower=None):
                    continue

                if not RentApplication.objects.filter(pk=pk, status=origin_application_status) \
                        .update(comments=comments, status=RentApplication.Status.REJECTED, applying=False):
                    continue
                break

        serializer = RentApplicationSerializer(rent_application)
        logger.info('change the status of the rent application: { id: ' + str(rent_application.id)
                    + ' } to rejected')
        email_address = RentApplication.objects.get(id=pk).borrower.email
        send_mail('[rental_platform.com] Please Check Your Application Status Updates'
                  , 'Hello from rental_platform.com!\n\n'
                    'You\'re receiving this e-mail because your RENT application for certain equipment: \n\n'
                    'name: ' + equipment.name +
                  '\nowner: ' + equipment.owner.first_name + ' ' + equipment.owner.last_name +
                  '\ndescription: ' + equipment.description +
                  '\nphone: ' + equipment.phone +
                  '\nemail: ' + equipment.email +
                  '\naddress: ' + equipment.address + '\n\n'
                                                      'has been REJECTED by the '
                                                      'administrator with comments as below: \n\n' + '"' + comments + '"' +
                  '\n\nThank you from rental_platform.com!\n'
                  'rental_platform.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='return')
    def return_post(self, request, pk):
        user_comments = request.POST.get('user_comments', '')

        with transaction.atomic():
            while True:
                try:
                    rent_application = RentApplication.objects.get(pk=pk)
                except RentApplication.DoesNotExist:
                    return Response({'detail': 'rent application not found'})

                if not rent_application.borrower.is_renter:
                    raise ValidationError(detail='borrower is not a renter', code=status.HTTP_400_BAD_REQUEST)

                origin_application_status = rent_application.status

                if origin_application_status != RentApplication.Status.ACCEPTED:
                    return Response({'detail': 'the rent application has not been accepted'}, status=status.HTTP_400_BAD_REQUEST)

                equipment = Equipment.objects.get(id=rent_application.equipment.id)
                origin_eq_status = equipment.status

                if origin_eq_status != Equipment.Status.RENTED:
                    return Response({'detail': 'the equipment is not rented'}, status=status.HTTP_400_BAD_REQUEST)

                if not Equipment.objects \
                        .filter(id=rent_application.equipment.id, status=origin_eq_status) \
                        .update(borrower=None, status=Equipment.Status.RETURNED):
                    continue

                if not RentApplication.objects \
                        .filter(pk=pk, status=origin_application_status)\
                        .update(user_comments=user_comments):
                    continue
                break

        rent_borrower = RentApplication.objects.get(id=pk).borrower
        email_address = equipment.owner.email
        send_mail('[rental_platform.com] Please Check Your Equipment\'s Newly Received Return Information'
                  , 'Hello from rental_platform.com!\n\n'
                    'You\'re receiving this e-mail because your equipment: \n\n'
                    'name: ' + equipment.name +
                  '\nowner: ' + equipment.owner.first_name + ' ' + equipment.owner.last_name +
                  '\ndescription: ' + equipment.description +
                  '\nphone: ' + equipment.phone +
                  '\nemail: ' + equipment.email +
                  '\naddress: ' + equipment.address + '\n\n'
                                                      'has been returned from: \n\n'
                  + '"' + rent_borrower.first_name + ' ' + rent_borrower.last_name + '"' +
                  '\n\nPlease check the current status of the equipment and re-release it if everything is fine. '
                  'If anything goes wrong, please contact the administrator.'
                  '\nThank you from rental_platform.com!\n'
                  'rental_platform.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)
        serializer = RentApplicationSerializer(rent_application)
        logger.info('change the status of the rent application: { id: ' + str(rent_application.id)
                    + ' } to returned and change the status of the equipment to returned')

        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='return/confirm')
    def return_confirm_post(self, request, pk):
        with transaction.atomic():
            while True:
                try:
                    rent_application = RentApplication.objects.get(pk=pk)
                except RentApplication.DoesNotExist:
                    return Response({'detail': 'rent application not found'}, status=status.HTTP_404_NOT_FOUND)

                origin_application_applying = rent_application.applying

                if not origin_application_applying:
                    return Response({'detail': 'the rent application is not applying'},
                                    status=status.HTTP_400_BAD_REQUEST)

                equipment = Equipment.objects.get(id=rent_application.equipment.id)
                origin_eq_status = equipment.status

                if origin_eq_status != Equipment.Status.RETURNED:
                    return Response({'detail': 'the equipment is not returned'}, status=status.HTTP_400_BAD_REQUEST)

                if not Equipment.objects \
                        .filter(id=rent_application.equipment.id, status=origin_eq_status) \
                        .update(status=Equipment.Status.AVAILABLE, borrower=None):
                    continue

                if not RentApplication.objects \
                        .filter(pk=pk, applying=origin_application_applying) \
                        .update(applying=False):
                    continue
                break

        serializer = RentApplicationSerializer(rent_application)
        logger.info('keep the status of the rent application: { id: ' + str(rent_application.id)
                    + ' } as returned and change the status of the equipment to available')
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


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from django_apscheduler.jobstores import register_job

try:
    # 实例化调度器

    scheduler = BackgroundScheduler(jobstores={
        'default': MemoryJobStore()
    })


    # 调度器使用DjangoJobStore()
    # scheduler.add_jobstore(DjangoJobStore(), "default")
    # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次
    @register_job(scheduler, 'interval', minutes=30, id='expire_reminder')
    def expire_reminder():
        utc_tz = pytz.timezone('UTC')
        rent_applications = RentApplication.objects.filter(applying=True)
        for rent_application in rent_applications:
            lease_term_end = rent_application.lease_term_end
            current_time = datetime.datetime.now(tz=utc_tz)
            seconds_delta = (lease_term_end - current_time).total_seconds()

            if seconds_delta > 60 * 60 * 24:
                continue

            if seconds_delta < 0:
                if rent_application.expired_reminded:
                    continue
                expire_message = 'has expired!'
                rent_application.expired_reminded = True
                rent_application.save()
            elif seconds_delta < 60 * 60:
                if rent_application.expire_before_hour_reminded:
                    continue
                expire_message = 'is going to expire in less than 1 hour!'
                rent_application.expire_before_hour_reminded = True
                rent_application.save()
            else:
                if rent_application.expire_before_day_reminded:
                    continue
                expire_message = 'is going to expire in less than 1 day!'
                rent_application.expire_before_day_reminded = True
                rent_application.save()

            send_mail('[rental_platform.com] Your Rented Equipment Is Going To Expire'
                      , 'Hello from rental_platform.com!\n\n'
                        'You\'re receiving this e-mail because your rented equipment [' + rent_application.equipment.name + '] '
                      + expire_message + ' Please return it timely!' +
                      '\n\nThank you from rental_platform.com!\n'
                      'rental_platform.com'
                      , '624275030@qq.com', [rent_application.borrower.email], fail_silently=False)


    # 调度器开始
    scheduler.start()
except:
    scheduler.shutdown()
