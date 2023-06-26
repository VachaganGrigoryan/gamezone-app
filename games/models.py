from django.db import models
from django.utils.translation import gettext_lazy as _


class Game(models.Model):
    guid = models.UUIDField(auto_created=True, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='games', blank=True, null=True)
    configs = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'games'

        verbose_name = _('Game')
        verbose_name_plural = _('Games')
        ordering = ['-pk']

    def __str__(self):
        return self.title
