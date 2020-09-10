from application.renter_application.models import RenterApplication
from application.renter_application.serializers import RenterApplicationSerializer
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import action

import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class RenterApplicationViewSet(viewsets.ModelViewSet):
    queryset = RenterApplication.objects.all()
    serializer_class = RenterApplicationSerializer

    filter_fields = '__all__'
    search_fields = ['description', 'comments']
    ordering_fields = '__all__'

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        renter_application = RenterApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        renter_application.update(comments=comments)
        renter_application.update(status='ACC')
        serializer = RenterApplicationSerializer(renter_application.first())
        logger.info('change the status of the renter application: { id: ' + str(renter_application.first().id)
                    + ' } to accepted')
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk):
        renter_application = RenterApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        renter_application.update(comments=comments)
        renter_application.update(status='REJ')
        serializer = RenterApplicationSerializer(renter_application.first())
        logger.info('change the status of the renter application: { id: ' + str(renter_application.first().id)
                    + ' } to rejected')
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
