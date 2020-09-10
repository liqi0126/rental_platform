from application.rent_application.models import RentApplication
from application.rent_application.serializers import RentApplicationSerializer
from equipment.models import Equipment
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import action


class RentApplicationViewSet(viewsets.ModelViewSet):
    queryset = RentApplication.objects.all()
    serializer_class = RentApplicationSerializer

    def perform_create(self, serializer):
        equipment_id = self.request.POST.get('equipment', '')
        try:
            equipment = Equipment.objects.get(id=equipment_id)
        except:
            return Response({'error': 'no such an equipment'}, status=400)

        serializer.save(renter=equipment.owner)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        rent_application = RentApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        rent_equipment = Equipment.objects.filter(id=rent_application.first().equipment.id)
        rent_equipment.update(status='REN')
        rent_application.update(comments=comments)
        rent_application.update(status='ACC')
        rent_application.update(applying=True)
        serializer = RentApplicationSerializer(rent_application.first())
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk):
        rent_application = RentApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        rent_application.update(comments=comments)
        rent_application.update(status='REJ')
        rent_application.update(applying=False)
        serializer = RentApplicationSerializer(rent_application.first())
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='return')
    def return_post(self, request, pk):
        rent_application = RentApplication.objects.filter(id=pk)
        user_comments = request.POST.get('user_comments', '')
        rent_application.update(user_comments=user_comments)
        rent_application.update(status='RET')
        rent_application.update(applying=False)
        rent_equipment = Equipment.objects.filter(id=rent_application.first().equipment.id)
        rent_equipment.update(status='RET')
        serializer = RentApplicationSerializer(rent_application.first())
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='return/confirm')
    def return_confirm_post(self, request, pk):
        rent_application = RentApplication.objects.filter(id=pk)
        release_equipment = Equipment.objects.filter(id=rent_application.first().equipment.id)
        release_equipment.update(status='AVA')
        serializer = RentApplicationSerializer(rent_application.first())
        return Response(serializer.data)

    filter_fields = '__all__'
    search_fields = ['description', 'comments', 'user_comments']
    ordering_fields = '__all__'
