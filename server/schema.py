from typing import List

import strawberry
from strawberry.django import auth

from jwtberry.mutations import auth_token
from jwtberry.types import JwtAuthResponse

from account.types import UserType, UserInput
from games.bazarblot.mutations import BazarblotMutation
from games.bazarblot.types import BazarblotQuery
from games.millionaire.mutations import MillionaireMutation
from games.millionaire.types import MillionaireQuery
from games.checkers.mutations import CheckersMutation
from games.checkers.types import CheckersQuery


@strawberry.type
class Query:
    users: List[UserType] = strawberry.django.field()
    user: UserType = strawberry.django.field()

    @strawberry.django.field()
    def millionaire(self) -> MillionaireQuery:
        return MillionaireQuery()

    @strawberry.django.field()
    def checkers(self) -> CheckersQuery:
        return CheckersQuery()

    @strawberry.django.field()
    def bazarblot(self) -> BazarblotQuery:
        return BazarblotQuery()


@strawberry.type
class Mutation:
    login: JwtAuthResponse = auth_token
    # refresh: JwtAuthResponse = refresh_token
    logout = auth.logout()
    register: UserType = auth.register(UserInput)

    @strawberry.django.field()
    def millionaire(self) -> MillionaireMutation:
        return MillionaireMutation()

    @strawberry.django.field()
    def checkers(self) -> CheckersMutation:
        return CheckersMutation()

    @strawberry.django.field()
    def bazarblot(self) -> BazarblotMutation:
        return BazarblotMutation()


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
