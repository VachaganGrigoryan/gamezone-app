from typing import Any, List, Optional
from datetime import timedelta
from django.conf import settings
from pydantic_settings import BaseSettings

from jwt_auth.consts import Algorithm


class JwtSettings(BaseSettings):
    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=5)
    REFRESH_TOKEN_LIFETIME: timedelta = timedelta(days=1)
    UPDATE_LAST_LOGIN: bool = False
    ALGORITHM: Algorithm = Algorithm.HS256
    SIGNING_KEY: str = settings.SECRET_KEY
    VERIFYING_KEY: str = ''
    AUDIENCE: Optional[str] = None
    ISSUER: Optional[str] = None
    JSON_ENCODER: Optional[str] = None
    JWK_URL: Optional[str] = None
    LEEWAY: timedelta = timedelta(seconds=0)
    AUTH_HEADER_TYPES: List[str] = ('Bearer',)
    AUTH_HEADER_NAME: str = "HTTP_AUTHORIZATION"
    USER_ID_FIELD: str = 'id'
    USER_ID_CLAIM: str = 'user_id'
    USER_AUTHENTICATION_RULE: str = 'jwt_auth.backends.default_user_authentication_rule'
    AUTH_TOKEN_CLASSES: List[str] = ('jwt_auth.tokens.AccessToken',)
    TOKEN_TYPE_CLAIM: str = 'token_type'
    JTI_CLAIM: str = 'jti'
    TOKEN_USER_CLASS: str = "rest_framework_simplejwt.models.TokenUser"

    class Config:
        env_prefix = 'JWT_'
        env_file_encoding = 'utf-8'
        case_sensitive = True

    # "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    # "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    # "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    # "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    # "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    # "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    # "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",


_jwt_settings = JwtSettings()
_jwt_settings_dict = _jwt_settings.model_dump()  # dict representation

# Allow users to override settings
if hasattr(settings, 'UserJwtAuthSettings'):
    _jwt_settings_dict.update(settings.UserJwtAuthSettings().model_dump())


def __dir__() -> List[str]:
    """The list of available options are retrieved from
    the dict view of our DjangoSettings object.
    """
    return list(_jwt_settings_dict.keys())


def __getattr__(name: str) -> Any:
    """Retrieve the value of a setting."""
    return _jwt_settings_dict[name]
