from typing import List

import strawberry
from strawberry.django import auth

from jwtberry.mutations import auth_token
from jwtberry.permission import IsAuthenticated
from jwtberry.types import JwtAuthResponse

from account.types import UserType, UserInput
from games.checkers.types import CheckersBoardType
from games.millionaire.mutations import MillionaireMutation
from games.millionaire.types import MillionaireQuery
from games.types import GameType
from games.checkers.mutations import create_board, update_board_in_game
from core.json import JSON
from games.checkers.game import get_board


import games.bazarblot.types


@strawberry.type
class Query(games.bazarblot.types.BazarBlotQuery):
    users: List[UserType] = strawberry.django.field()
    user: UserType = strawberry.django.field()

    @strawberry.django.field()
    def millionaire(self) -> MillionaireQuery:
        return MillionaireQuery()

    checkers: List[CheckersBoardType] = strawberry.django.field()

    @strawberry.django.field(permission_classes=[IsAuthenticated])
    def games(self, info) -> List[GameType]:
        return GameType.all(info)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info) -> UserType:
        return info.context.user
    
    # get board state
    @strawberry.field
    def resolve_board_state(self, info, guid: str) -> JSON:
        return get_board(guid)


@strawberry.type
class Mutation:
    login: JwtAuthResponse = auth_token
    # refresh: JwtAuthResponse = refresh_token
    logout = auth.logout()
    register: UserType = auth.register(UserInput)
    create_board: JSON = create_board
    update_board_in_game: JSON = update_board_in_game

    @strawberry.django.field()
    def millionaire(self) -> MillionaireMutation:
        return MillionaireMutation()


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
