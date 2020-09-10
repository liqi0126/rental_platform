from application.release_application.models import ReleaseApplication
from application.release_application.serializers import ReleaseApplicationSerializer
from equipment.models import Equipment
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import action


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
        serializer.save(owner=equipment.owner)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk):
        release_application = ReleaseApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        release_application.update(comments=comments)
        release_application.update(status='ACC')
        release_equipment = Equipment.objects.filter(id=release_application.first().equipment.id)
        release_equipment.update(status='AVA')
        serializer = ReleaseApplicationSerializer(release_application.first())
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk):
        release_application = ReleaseApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        release_application.update(comments=comments)
        release_application.update(status='REJ')
        serializer = ReleaseApplicationSerializer(release_application.first())
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk):
        release_application = ReleaseApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        release_application.update(comments=comments)
        release_application.update(status='REJ')
        serializer = ReleaseApplicationSerializer(release_application.first())
        return Response(serializer.data)
