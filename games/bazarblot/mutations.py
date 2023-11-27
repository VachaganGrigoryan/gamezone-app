import strawberry
from asgiref.sync import sync_to_async
from django.db import transaction
from jwtberry.permission import IsAuthenticated
from strawberry.types import Info

from games.bazarblot import models as m
from games.bazarblot.types import Table


@strawberry.type
class BazarblotMutation:

    @strawberry.mutation(
        permission_classes=[IsAuthenticated]
    )
    @sync_to_async
    def create_table(self, info: Info) -> Table:
        user = info.context.user

        with transaction.atomic():
            team = m.Team.objects.create()
            team.players.set([user])

            table = m.Table.objects.create(
                players_order=[str(user.guid)]
            )
            table.teams.set([team])

        return table

    @strawberry.mutation(
        permission_classes=[IsAuthenticated]
    )
    @sync_to_async
    def join_to_table(self, info: Info, guid: strawberry.ID) -> str:
        user = info.context.user

        table = m.Table.objects.filter(
            guid=guid, is_active=True
        ).first()

        if table is None:
            return "Can't find table."

        if len(table.players_order) == 4:
            return "You can't join into table."

        if any([user in team.players.all() for team in table.teams.all()]):
            return table

        with transaction.atomic():
            if table.players_order == 1:
                team = m.Team.objects.create()
                team.players.set([user])
                table.teams.add(team)
            elif table.players_order == 2:
                team_one = table.teams.first()
                team_one.add(user)
            else:
                team_two = table.teams.last()
                team_two.add(user)

            table.players_order.append(str(user.guid))
            table.save()

        return table
