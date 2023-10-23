from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class JWTToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    jti = models.CharField(unique=True, max_length=255)
    refresh_token = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'jwt_tokens'

        abstract = ('jwt_auth.jwt_token' not in settings.INSTALLED_APPS)

        verbose_name = _('JWT Token')
        verbose_name_plural = _('JWT Tokens')

    def __str__(self):
        return f'Token for {self.user} - ({self.jti})'


class JWTBlacklist(models.Model):
    token = models.OneToOneField(
        JWTToken,
        on_delete=models.CASCADE
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jwt_blacklist'

        abstract = ('jwt_auth.jwt_token' not in settings.INSTALLED_APPS)

        verbose_name = _('JWT Blacklist')
        verbose_name_plural = _('JWT Blacklists')
