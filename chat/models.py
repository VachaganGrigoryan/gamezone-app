from django.db import models
from django.utils.translation import gettext_lazy as _

class Chat(models.Model):

    guid = models.UUIDField(auto_created=True, unique=True, db_index=True)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE) 
    game_guid = models.UUIDField(db_index=True, unique=True)
    members = models.ManyToManyField(
        'account.User',
        verbose_name=_('Members')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat'
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')


class Message(models.Model):

    guid = models.UUIDField(auto_created=True, unique=True, db_index=True)
    sender = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name=_('Sender'))
    message = models.TextField(max_length=255)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
