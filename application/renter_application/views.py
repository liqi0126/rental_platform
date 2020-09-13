from django.db import transaction
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets, permissions


from user.models import User
from application.permission import IsAdminOrCannotUpdateAndDestroy
from application.renter_application.models import RenterApplication
from application.renter_application.serializers import RenterApplicationSerializer

import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class RenterApplicationViewSet(viewsets.ModelViewSet):
    queryset = RenterApplication.objects.all()
    serializer_class = RenterApplicationSerializer
    permission_classes = [IsAdminOrCannotUpdateAndDestroy]

    filter_fields = '__all__'
    search_fields = ['description', 'comments']
    ordering_fields = '__all__'

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk):
        comments = request.POST.get('comments', '')
        try:
            renter_application = RenterApplication.objects.get(id=pk)
        except RenterApplication.DoesNotExist:
            return Response({'detail': 'renter application not found'}, status=status.HTTP_404_NOT_FOUND)

        # atomic
        with transaction.atomic():
            renter_application.comments = comments
            renter_application.status = RenterApplication.Status.ACCEPTED
            renter_application.save()
            renter = User.objects.get(id=renter_application.applicant.id)
            renter.is_renter = True
            renter.save()

        serializer = RenterApplicationSerializer(renter_application)
        logger.info('change the status of the renter application: { id: ' + str(renter_application.id)
                    + ' } to accepted')
        email_address = renter_application.applicant.email
        send_mail('[rental_platform.com] Please Check Your Application Status Updates'
                  , 'Hello from rental_platform.com!\n\n'
                    'You\'re receiving this e-mail because your RENTER application has been APPROVED by the '
                    'administrator with comments as below: \n\n' + '"' + comments + '"' +
                    '\n\nThank you from rental_platform.com!\n'
                    'rental_platform.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk):
        try:
            renter_application = RenterApplication.objects.get(pk=pk)
        except RenterApplication.DoesNotExist:
            return Response({'detail': 'renter application not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = request.POST.get('comments', '')
        with transaction.atomic():
            renter_application.comments = comments
            renter_application.status = RenterApplication.Status.REJECTED
            renter_application.save()
            renter = User.objects.get(id=renter_application.applicant.id)
            renter.is_renter = False
            renter.save()

        serializer = RenterApplicationSerializer(renter_application)
        logger.info('change the status of the renter application: { id: ' + str(renter_application.id)
                    + ' } to rejected')
        email_address = RenterApplication.objects.get(pk=pk).applicant.email
        send_mail('[rental_platform.com] Please Check Your Application Status Updates'
                  , 'Hello from rental_platform.com!\n\n'
                    'You\'re receiving this e-mail because your RENTER application has been REJECTED by the '
                    'administrator with comments as below: \n\n' + '"' + comments + '"' +
                  '\n\nThank you from rental_platform.com!\n'
                  'rental_platform.com'
                  , '624275030@qq.com', [email_address], fail_silently=False)
        return Response(serializer.data)

    def perform_create(self, serializer):
        logger.info('create a new renter application: ' + str(serializer.validated_data))
        serializer.save()

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            logger.info('update a renter application(through put): ' + str(serializer.validated_data))
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info('update a renter application(through patch): ' + str(request.data))
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        logger.info('delete a renter application: ' + str(instance))
        instance.delete()
