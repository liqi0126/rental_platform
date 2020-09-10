from application.renter_application.models import RenterApplication
from application.renter_application.serializers import RenterApplicationSerializer
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import action


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
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk):
        renter_application = RenterApplication.objects.filter(id=pk)
        comments = request.POST.get('comments', '')
        renter_application.update(comments=comments)
        renter_application.update(status='REJ')
        serializer = RenterApplicationSerializer(renter_application.first())
        return Response(serializer.data)
