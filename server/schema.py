import strawberry
from strawberry.django import auth
from typing import List

from account.types import UserType, UserInput
from games.checkers.types import CheckersBoardType
from games.types import GameType


@strawberry.type
class Query:
    users: List[UserType] = strawberry.django.field()
    user: UserType = strawberry.django.field()

    games: List[GameType] = strawberry.django.field()

    checkers: List[CheckersBoardType] = strawberry.django.field()


@strawberry.type
class Mutation:
    login: UserType = auth.login()
    logout = auth.logout()
    register: UserType = auth.register(UserInput)


schema = strawberry.Schema(query=Query, mutation=Mutation)
