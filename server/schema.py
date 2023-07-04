from typing import List

import strawberry
from strawberry.django import auth

from jwt_auth.decorators import login_required
from jwt_auth.extension import AsyncJwtExtension
from jwt_auth.mutations import auth_token, refresh_token

from account.types import UserType, UserInput
from games.checkers.types import CheckersBoardType
from games.types import GameType
from jwt_auth.types import JwtAuthResponse


@strawberry.type
class Query:
    users: List[UserType] = strawberry.django.field()
    user: UserType = strawberry.django.field()

    # games: List[GameType] = login_required(strawberry_django.field())

    checkers: List[CheckersBoardType] = strawberry.django.field()

    @strawberry.django.field
    @login_required
    def games(self, info) -> List[GameType]:
        return GameType.all(info)

    @strawberry.field
    @login_required
    def me(self, info) -> UserType:
        return info.context.user


@strawberry.type
class Mutation:
    login: JwtAuthResponse = auth_token
    refresh: JwtAuthResponse = refresh_token
    logout = auth.logout()
    register: UserType = auth.register(UserInput)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        AsyncJwtExtension,  # JwtExtension,
    ],
)
