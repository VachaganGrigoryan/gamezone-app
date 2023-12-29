import strawberry
from strawberry.django import auth

from account.mutations import AccountMutation
from account.types import AccountQuery
from games.bazarblot.mutations import BazarblotMutation
from games.bazarblot.types import BazarblotQuery
from games.millionaire.mutations import MillionaireMutation
from games.millionaire.types import MillionaireQuery
from games.checkers.mutations import CheckersMutation
from games.checkers.types import CheckersQuery
from games.types import ZoneQuery


@strawberry.type
class Query:

    @strawberry.django.field()
    def account(self) -> AccountQuery:
        return AccountQuery()

    @strawberry.django.field()
    def zone(self) -> ZoneQuery:
        return ZoneQuery()

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

    @strawberry.django.field()
    def account(self) -> AccountMutation:
        return AccountMutation()

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
