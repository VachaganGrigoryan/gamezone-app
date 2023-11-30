import datetime
from typing import Optional

import strawberry
from asgiref.sync import sync_to_async
from django.db import transaction
from jwtberry.permission import IsAuthenticated
from strawberry.types import Info

from account.models import User
from games.bazarblot import models as m
from games.bazarblot.choices import GamePoint
from games.bazarblot.game import Game, BazarValidation, Suit
from games.bazarblot.inputs import CardInput
from games.bazarblot.types import Table, Bazar, Contra, ReContra


# from games.bazarblot.utils import start_game


@strawberry.type
class BazarblotMutation:

    @strawberry.mutation(
        permission_classes=[IsAuthenticated]
    )
    @sync_to_async
    def create_table(self, info: Info) -> Table:
        user = info.context.user
        now = datetime.datetime.now()
        with transaction.atomic():
            team = m.Team.objects.create()
            team.players.set([user])

            table = m.Table.objects.create(
                players_order=[str(user.guid)],
                # max_points=max_points,
                created_at=now,
                updated_at=now,
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
            # harcery kluciq
            return table

        with transaction.atomic():
            if len(table.players_order) == 1:
                team = m.Team.objects.create()
                team.players.set([user])
                table.teams.add(team)
            elif len(table.players_order) == 2:
                team_one = table.teams.first()
                team_one.players.add(user)
            else:
                team_two = table.teams.last()
                team_two.players.add(user)

            table.players_order.append(str(user.guid))
            table.save()

            if len(table.players_order) == 4:
                first_round = m.Round.objects.create(
                    table=table,
                    order=1,
                )

                deck = Game.build_deck()
                for i, player_user in enumerate(User.objects.filter(guid__in=table.players_order)):
                    m.RoundPlayersCards.objects.create(
                        round=first_round,
                        player=player_user,
                        cards=deck[i * 8:(i + 1) * 8]
                    )
        return table

    @strawberry.mutation(
        permission_classes=[IsAuthenticated]
    )
    @sync_to_async
    @transaction.atomic
    def bazar(self, info, table_guid: strawberry.ID, round_pk: strawberry.ID, card: Optional[CardInput] = None,
              value: str = "PASS") -> Bazar:
        player = info.context.user
        table = m.Table.objects.get(guid=table_guid)
        game_round = m.Round.objects.get(pk=round_pk)
        bazars = list(game_round.bazars.all())
        length = len(bazars)
        if game_round.trump_suit:
            raise ValueError("Round is playing")
        if length % 4 != table.players_order.index(str(player.guid)):
            raise ValueError("Invalid queue")

        validation_result = BazarValidation(bazars, player).validate(card, value)
        if not validation_result:
            raise ValueError("Invalid bazar")
        elif validation_result == '4 pass':
            game_round.trump_suit = length >= 4 and bazars[3].value or "No suit"
            game_round.save()

        if value == "PASS":
            value = "0"
        elif "K" in value:
            value = f'-{value[:-1]}'

        bazar = m.Bazar.objects.create(
            round=game_round,
            player=player,
            card=card,
            value=value,
            order=length + 1,
        )

        return bazar

    @strawberry.mutation(
        permission_classes=[IsAuthenticated]
    )
    @sync_to_async
    @transaction.atomic
    def contra(self, info, table_guid: strawberry.ID, round_pk: strawberry.ID) -> Contra:
        game_round = m.Round.objects.get(pk=round_pk)
        table = m.Table.objects.get(guid=table_guid)
        player = info.context.user
        bazars = game_round.bazars.all()
        length = len(bazars)

        if length % 2 != table.players_order.index(str(player.guid)) % 2:
            raise ValueError("Invalid queue")

        cntr = m.Contra.objects.create(
            bazar=list(bazars)[-1],
            player=player,
        )
        return cntr

    @strawberry.mutation(
        permission_classes=[IsAuthenticated]
    )
    @sync_to_async
    @transaction.atomic
    def re_contra(self, info, table_guid: strawberry.ID, round_pk: strawberry.ID) -> ReContra:
        game_round = m.Round.objects.get(pk=round_pk)
        player = info.context.user
        bazars = game_round.bazars.all()
        last_bazar = list(bazars)[-1]
        if not hasattr(last_bazar, "contra"):
            raise ValueError("No contra")

        table = m.Table.objects.get(guid=table_guid)
        length = len(bazars)

        if length % 2 == table.players_order.index(str(player.guid)) % 2:
            raise ValueError("Invalid queue")

        contra = m.Contra.objects.get(bazar=last_bazar)
        re_cntr = m.ReContra.objects.create(
            contra=contra,
            player=player,
        )
        return re_cntr
