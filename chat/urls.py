from django.urls import path

from .views import *


urlpatterns = [

    path(
        'create-conversation/',
        create_conversation
    ),

    path(
        'send-message/',
        send_message
    ),

    path(
        'conversations/',
        get_conversations
    ),

    path(
        'messages/<int:conversation_id>/',
        get_messages
    ),

    path(
        'seen-message/',
        seen_message
    ),
]