from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from equipment.models import Equipment
from equipment.serializers import EquipmentSerializer


import logging

logger = logging.getLogger(__name__)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    filter_fields = '__all__'
    search_fields = ['name', 'address', 'description']
    ordering_fields = '__all__'

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk):
        while True:
            try:
                equipment = Equipment.objects.get(pk=pk)
            except Equipment.DoesNotExist:
                return Response({'detail': 'equipment not found'}, status=status.HTTP_404_NOT_FOUND)

            origin_eq_status = equipment.status

            if origin_eq_status != Equipment.Status.AVAILABLE:
                return Response({'detail': 'cannot withdraw the equipment when it is not available'}, status=status.HTTP_400_BAD_REQUEST)

            Equipment.objects.filter(pk=pk, status=origin_eq_status).update(status=Equipment.Status.UNRELEASED, is_released=False)
            break

        return Response('ok')

    def perform_create(self, serializer):
        logger.info('create a new equipment: { name: ' + str(serializer.validated_data.get('name')) + ' }')
        serializer.save()

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            logger.info('update an equipment(through put): { name: ' + str(serializer.validated_data.get('name'))
                        + ' }')
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info('update an equipment(through patch): ' + str(request.data))
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        logger.info('delete an equipment: { name: ' + str(instance) + ' }')
        instance.delete()
