from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import *


# =========================================
# CREATE CONVERSATION
# =========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_conversation(request):

    user_id = request.data.get('user_id')

    other_user = User.objects.get(id=user_id)

    # check existing chat
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user,
        is_group=False
    ).first()

    if conversation:

        return Response({
            'conversation_id': conversation.id,
            'message': 'already exists'
        })

    # create new conversation
    conversation = Conversation.objects.create()

    conversation.participants.add(
        request.user,
        other_user
    )

    return Response({
        'conversation_id': conversation.id,
        'message': 'conversation created'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):

    conversation_id = request.data.get(
        'conversation_id'
    )

    text = request.data.get('text')

    conversation = Conversation.objects.get(
        id=conversation_id
    )

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        text=text,
        message_type='text'
    )

    # update last message
    conversation.last_message = message
    conversation.save()

    return Response({

        'message_id': message.id,

        'text': message.text,

        'sender': message.sender.username,

        'conversation_id': conversation.id,

        'created_at': message.created_at
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversations(request):

    conversations = Conversation.objects.filter(
        participants=request.user
    ).order_by('-updated_at')

    data = []

    for conversation in conversations:

        participants = []

        for user in conversation.participants.all():

            participants.append({
                'id': user.id,
                'username': user.username
            })

        data.append({

            'conversation_id': conversation.id,

            'participants': participants,

            'is_group': conversation.is_group,

            'group_name': conversation.group_name,

            'last_message':

                conversation.last_message.text

                if conversation.last_message

                else None,

            'updated_at': conversation.updated_at
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, conversation_id):

    messages = Message.objects.filter(
        conversation_id=conversation_id
    ).order_by('created_at')

    data = []

    for message in messages:

        data.append({

            'id': message.id,

            'sender': message.sender.username,

            'sender_id': message.sender.id,

            'text': message.text,

            'message_type': message.message_type,

            'is_seen': message.is_seen,

            'created_at': message.created_at
        })

    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seen_message(request):

    message_id = request.data.get('message_id')

    message = Message.objects.get(id=message_id)

    MessageSeen.objects.get_or_create(
        message=message,
        user=request.user
    )

    message.is_seen = True
    message.save()

    return Response({
        'message': 'seen'
    })

