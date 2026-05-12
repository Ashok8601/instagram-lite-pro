from django.db import models
from django.contrib.auth.models import User


# =========================
# Conversation Model
# =========================

class Conversation(models.Model):

    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    last_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='last_message_conversation'
    )

    is_group = models.BooleanField(default=False)

    group_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    group_image = models.ImageField(
        upload_to='group_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        if self.is_group:
            return self.group_name

        return f"Conversation {self.id}"


# =========================
# Message Model
# =========================

class Message(models.Model):

    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('voice', 'Voice'),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    text = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='chat_images/',
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to='chat_videos/',
        blank=True,
        null=True
    )

    voice = models.FileField(
        upload_to='voice_notes/',
        blank=True,
        null=True
    )

    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default='text'
    )

    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )

    is_seen = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.conversation.id}"


# =========================
# Message Seen Model
# =========================

class MessageSeen(models.Model):

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='seen_by'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    seen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['message', 'user']

    def __str__(self):
        return f"{self.user.username} seen {self.message.id}"


# =========================
# User Online Status
# =========================

class UserStatus(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='status'
    )

    is_online = models.BooleanField(default=False)

    last_seen = models.DateTimeField(
        blank=True,
        null=True
    )

    typing_in = models.ForeignKey(
        Conversation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
