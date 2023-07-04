from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JwtTokenConfig(AppConfig):
    name = "jwt_auth.jwt_token"
    verbose_name = _("JWT Token")
    default_auto_field = "django.db.models.BigAutoField"
