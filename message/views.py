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

    @action(detail=False, methods=['get'], url_path='chats')
    def chats(self, request):
        id_one = request.GET.get('id_one')
        id_two = request.GET.get('id_two')
        print(id_one)
        print(id_two)
        try:
            chatter_one = User.objects.get(id=id_one)
        except:
            return Response({'error': 'id_one is not valid'}, status=400)
        try:
            chatter_two = User.objects.get(id=id_two)
        except:
            return Response({'error': 'id_two is not valid'}, status=400)
        chat_condition_asc = {'sender': chatter_one, 'receiver': chatter_two}
        chat_condition_desc = {'sender': chatter_two, 'receiver': chatter_one}
        chat_messages = Message.objects.filter(Q(**chat_condition_asc) | Q(**chat_condition_desc))
        logger.info('get chat messages between ' + chatter_one.first_name + ' ' + chatter_one.last_name
                    + ' and ' + chatter_two.first_name + ' ' + chatter_two.last_name )
        serializer = MessageSerializer(chat_messages, many=True)
        return Response(serializer.data)

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
