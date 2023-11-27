from typing import List, Optional

import strawberry
from jwtberry.permission import IsAuthenticated
from strawberry import auto
from strawberry.types import Info

from account.types import UserType
from core.json import JSON
from games.bazarblot import models as m


@strawberry.django.type(m.Team)
class Team:
    score: int

    @strawberry.django.field()
    def players(self) -> List[UserType]:
        print(self.players.all())
        return self.players.all()


@strawberry.django.type(m.Table)
class Table:
    guid: strawberry.ID

    teams: List[Team]

    max_points: auto
    created_at: auto
    updated_at: auto
    is_ended: auto

    players_order: Optional[JSON] = None
    winner: Optional[UserType] = None

    @classmethod
    def all(cls, info) -> List[m.Table]:
        return m.Table.objects.all()


@strawberry.type
class BazarblotQuery:

    @strawberry.django.field(
        # permission_classes=[IsAuthenticated]
    )
    def tables(self, info: Info) -> List[Table]:
        return Table.all(info)
