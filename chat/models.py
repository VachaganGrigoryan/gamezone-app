import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Chat(models.Model):
    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier.'),
    )
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE) 
    game_guid = models.UUIDField(db_index=True, unique=True)
    members = models.ManyToManyField(
        'account.User',
        verbose_name=_('Members'),
        through='ChatMembers',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat'
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')


class ChatMembers(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('chat', 'user')


class Message(models.Model):
    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True,
        verbose_name=_('GUID'),
        help_text=_('The unique identifier.'),
    )
    sender = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name=_('Sender'))
    message = models.TextField(max_length=255)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
