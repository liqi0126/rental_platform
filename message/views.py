from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from message.models import Message
from user.models import User
from message.serializers import MessageSerializer

from django.db.models import Q
import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    filter_fields = '__all__'
    search_fields = ['text']
    ordering_fields = '__all__'

    # # TODO: get messages from both side
    # @action(detail=True, methods=['get'])
    # def chats(self, request, sender_id, receiver_id):
    #     sender = User.objects.get(id=sender_id)
    #     receiver = User.objects.get(id=receiver_id)
    #     chat_condition_asc = {'sender': sender, 'receiver': receiver}
    #     chat_condition_desc = {'sender': receiver, 'receiver': sender}
    #     chat_messages = Message.objects.all()
    #     # chat_messages = Message.objects.filter(Q(**chat_condition_asc) | Q(**chat_condition_desc))
    #     serializer = MessageSerializer(chat_messages)
    #     return Response(serializer.data)

    # TODO
    def perform_create(self, serializer):
        logger.info('create a new chat message: { sender: ' + str(serializer.validated_data.get('sender'))
                    + ', receiver: ' + str(serializer.validated_data.get('receiver'))
                    + ', text: ' + str(serializer.validated_data.get('text')) + ' }')
        serializer.save()

    # TODO
    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            logger.info('update a chat message(through put): { sender: ' + str(serializer.validated_data.get('sender'))
                        + ', receiver: ' + str(serializer.validated_data.get('receiver'))
                        + ', text: ' + str(serializer.validated_data.get('text')) + ' }')
        serializer.save()

    # TODO
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        logger.info('update a chat message(through patch): ' + str(request.data))
        return self.update(request, *args, **kwargs)

    # TODO
    def perform_destroy(self, instance):
        logger.info('delete a chat message: ' + str(instance))
        instance.delete()
