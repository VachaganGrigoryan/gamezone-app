from typing import List, Optional

import strawberry
from jwtberry.permission import IsAuthenticated
from strawberry import auto
from strawberry.types import Info

from account.types import UserType
from core.json import JSON
from games.bazarblot import models as m
from games.bazarblot.game import Rank, Suit
from games.bazarblot.inputs import CardInput


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

    rounds: "Round"
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


@strawberry.django.type(m.Round)
class Round:
    pk: strawberry.ID

    is_active: auto
    trump_suit: strawberry.enum(Suit)
    order: auto


@strawberry.type
class Card:
    rank: strawberry.enum(Rank)
    suit: strawberry.enum(Suit)


@strawberry.django.type(m.Bazar)
class Bazar:
    pk: strawberry.ID

    round: Round
    player: UserType

    card: Card
    value: auto


@strawberry.django.type(m.Contra)
class Contra:
    bazar: Bazar
    player: UserType


@strawberry.django.type(m.ReContra)
class ReContra:
    contra: Contra
    player: UserType


@strawberry.type
class BazarblotQuery:

    @strawberry.django.field(
        # permission_classes=[IsAuthenticated]
    )
    def tables(self, info: Info) -> List[Table]:
        return Table.all(info)
