from typing import List

import strawberry

from account.types import UserType
from games.checkers import models
from games.types import GameType
from jwtberry.permission import IsAuthenticated
from games.checkers.game import get_board
from core.json import JSON


@strawberry.django.type(models.Board)
class CheckersBoardType:
    guid: strawberry.ID
    players: List[UserType]
    queue: UserType
    winner: UserType
    grid: List[List[int]]
    length: int
    is_ended: bool

    created_at: str
    updated_at: str

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_active=True)


@strawberry.django.type(models.Histories)
class CheckersHistoriesType:
    guid: strawberry.ID
    board: CheckersBoardType
    player: UserType

    from_point: List[int]
    to_point: List[int]
    taken_points: List[List[int]]

    played_at: str

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_active=True)


@strawberry.type
class CheckersQuery:

    checkers: List[CheckersBoardType] = strawberry.django.field()

    def games(self, info) -> List[GameType]:
        return GameType.all(info)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info) -> UserType:
        return info.context.user
    
    # get board state
    @strawberry.field
    def resolve_board_state(self, info, guid: str) -> JSON:
        return get_board(guid)
