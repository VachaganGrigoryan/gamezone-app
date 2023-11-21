from typing import List

import strawberry
from strawberry.django import auth

from jwtberry.mutations import auth_token
from jwtberry.permission import IsAuthenticated
from jwtberry.types import JwtAuthResponse

from account.types import UserType, UserInput
from games.checkers.types import CheckersBoardType
from games.types import GameType


import games.bazarblot.types


@strawberry.type
class Query(games.bazarblot.types.BazarBlotQuery):
    users: List[UserType] = strawberry.django.field()
    user: UserType = strawberry.django.field()

    # games: List[GameType] = login_required(strawberry_django.field())

    checkers: List[CheckersBoardType] = strawberry.django.field()

    @strawberry.django.field(permission_classes=[IsAuthenticated])
    def games(self, info) -> List[GameType]:
        return GameType.all(info)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info) -> UserType:
        return info.context.user


@strawberry.type
class Mutation:
    login: JwtAuthResponse = auth_token
    # refresh: JwtAuthResponse = refresh_token
    logout = auth.logout()
    register: UserType = auth.register(UserInput)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
