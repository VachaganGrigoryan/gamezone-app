from typing import List, Optional

import strawberry
from strawberry import auto
from strawberry.types import Info
from strawberry_django import django_resolver

from account.types import UserType
from games.checkers import models as m
from jwtberry.permission import IsAuthenticated


@strawberry.django.type(m.BoardPlayers)
class BoardPlayers:
    player: UserType
    stone_type: auto


@strawberry.django.type(m.Board)
class CheckersBoardType:
    guid: strawberry.ID
    queue: UserType
    winner: Optional[UserType]
    grid: List[List[int]]
    length: int
    is_ended: bool

    created_at: str
    updated_at: str

    @strawberry.field()
    @django_resolver
    def players(self) -> List[BoardPlayers]:
        return self.boardplayers_set.all()

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_active=True)

    @classmethod
    def all(cls, info) -> List[m.Board]:
        return m.Board.objects.all()

    @classmethod
    async def get_object_by_guid(cls, info, guid) -> m.Board:
        return await m.Board.objects.prefetch_related('boardplayers_set').filter(guid=guid).afirst()


@strawberry.django.type(m.Histories)
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

    @strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
    async def game(self, info: Info, guid: str) -> CheckersBoardType:
        return await CheckersBoardType.get_object_by_guid(info, guid)


    @strawberry.django.field(
        permission_classes=[IsAuthenticated]
    )
    def boards(self, info: Info) -> List[CheckersBoardType]:
        return CheckersBoardType.all(info)