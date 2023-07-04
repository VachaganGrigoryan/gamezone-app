from typing import Any

import strawberry
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.module_loading import import_string
from strawberry.types import Info

from jwt_auth import settings
from jwt_auth.auth import authenticate
from jwt_auth.tokens import RefreshToken
from jwt_auth.types import TokenType, AuthenticationFailed


@strawberry.mutation
async def auth_token(info: Info, email: str, password: str) -> Any:
    auth_kwargs = {
        get_user_model().USERNAME_FIELD: email,
        'password': password,
    }

    try:
        auth_kwargs['request'] = info.context.request
    except AttributeError:
        pass

    user = await authenticate(**auth_kwargs)

    auth_rule = import_string(settings.USER_AUTHENTICATION_RULE)
    if not auth_rule(user):
        return AuthenticationFailed(
            detail='Invalid Credentials or inactive user',
            code='authentication_failed',
        )

    refresh = RefreshToken.create(user)

    data = TokenType(
        access=str(refresh.access_token),
        refresh=str(refresh),
    )

    if settings.UPDATE_LAST_LOGIN:
        update_last_login(None, user)

    return data


@strawberry.mutation
async def refresh_token(info: Info, refresh: str) -> Any:
    ...
