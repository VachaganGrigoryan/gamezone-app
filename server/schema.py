from typing import List

import strawberry
from strawberry.django import auth

from jwtberry.mutations import auth_token
from jwtberry.permission import IsAuthenticated
from jwtberry.types import JwtAuthResponse

from account.types import UserType, UserInput
from games.millionaire.mutations import MillionaireMutation
from games.millionaire.types import MillionaireQuery
from games.checkers.mutations import CheckersMutation
from games.checkers.types import CheckersQuery
from core.json import JSON


import games.bazarblot.types


@strawberry.type
class Query(games.bazarblot.types.BazarBlotQuery):
    users: List[UserType] = strawberry.django.field()
    user: UserType = strawberry.django.field()

    @strawberry.django.field()
    def millionaire(self) -> MillionaireQuery:
        return MillionaireQuery()
    

    # added queries by Samvel
    @strawberry.django.field()
    def checkers(self) -> CheckersQuery:
        return CheckersQuery()
    
    # checkers: List[CheckersBoardType] = strawberry.django.field()

    # @strawberry.django.field(permission_classes=[IsAuthenticated])
    # def games(self, info) -> List[GameType]:
    #     return GameType.all(info)

    # @strawberry.field(permission_classes=[IsAuthenticated])
    # def me(self, info) -> UserType:
    #     return info.context.user
    
    # # get board state
    # @strawberry.field
    # def resolve_board_state(self, info, guid: str) -> JSON:
    #     return get_board(guid)


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


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
