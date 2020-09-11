from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from message.models import Message
from message.serializers import MessageSerializer


import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    filter_fields = '__all__'
    search_fields = ['text']
    ordering_fields = '__all__'

    # TODO: get messages from both side
    @action(detail=True, methods=['get'])
    def chats(self, request, pk):
        pass

    # TODO
    def perform_create(self, serializer):
        pass
        serializer.save()

    # TODO
    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            logger.info('update an equipment(through put): { name: ' + str(serializer.validated_data.get('name'))
                        + ' }')
        serializer.save()

    # TODO
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info('update an equipment(through patch): ' + str(request.data))
        return self.update(request, *args, **kwargs)


    # TODO
    def perform_destroy(self, instance):
        logger.info('delete an equipment: { name: ' + str(instance) + ' }')
        instance.delete()
