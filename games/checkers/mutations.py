from typing import List

import strawberry
from asgiref.sync import sync_to_async
from django.db import transaction
from jwtberry.permission import IsAuthenticated
from strawberry.types import Info

from core.json import JSON

from games.checkers import models as m
from games.checkers.choices import BoardLength
from games.checkers.game import update_board, CC
from games.checkers.types import CheckersBoardType
from games.checkers.utils import init_board


@strawberry.type
class CheckersMutation:

    @strawberry.django.mutation(
        permission_classes=[IsAuthenticated]
    )
    @transaction.atomic
    def start(
        self,
        info: Info,
        color: strawberry.enum(CC) = CC.White,
        length: strawberry.enum(BoardLength) = BoardLength.EIGHT
    ) -> CheckersBoardType:
        user = info.context.user
        grid = init_board(length)

        board = m.Board.objects.create(
            owner=user,
            queue=user if color == CC.White else None,
            grid=grid,
        )
        m.BoardPlayers.objects.create(
            board=board,
            player=user,
            stone_type=2 if color == CC.White else 3
        )

        return board

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def update_board_in_game(self, guid: strawberry.ID, grid_changes: List[List[int]]) -> JSON:
        return update_board(guid=guid, grid_changes=grid_changes)
