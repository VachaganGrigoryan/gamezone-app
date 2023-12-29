from typing import List

import strawberry
from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.models import Count, Q
from jwtberry.permission import IsAuthenticated
from strawberry.types import Info

from core.json import JSON

from games.checkers import models as m
from games.checkers.choices import BoardLength
from games.checkers.game import update_board, CC, Game
from games.checkers.types import Board
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
    ) -> Board:
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

    @strawberry.django.mutation(
        permission_classes=[IsAuthenticated]
    )
    @transaction.atomic
    def join(self, info: Info, guid: strawberry.ID) -> Board:
        user = info.context.user
        board = m.Board.objects.annotate(players_count=Count("boardplayers")).filter(
            Q(guid=guid) & ~Q(owner=user) & Q(players_count=1)
        ).first()

        if board is None:
            raise ValueError("Cant find board or it's already have two players")

        stone_type = 3
        if board.queue is None:
            board.queue = user
            stone_type = 2

        board.save()

        m.BoardPlayers.objects.create(
            board=board,
            player=user,
            stone_type=stone_type
        )

        return board

    @strawberry.django.mutation(
        permission_classes=[IsAuthenticated]
    )
    @transaction.atomic
    def move(self, info: Info, guid: strawberry.ID, moves: List[List[int]]) -> Board:
        user = info.context.user
        board = m.Board.objects.annotate(players_count=Count("boardplayers")).filter(
            Q(guid=guid) & Q(queue=user) & Q(players_count=2)
        ).first()

        if board is None:
            raise ValueError("Cant find board or queue is not yours")

        player_queue = m.BoardPlayers.objects.get(player=user, board=board)

        game = Game(board.grid, player_queue.stone_type)
        is_valid, errors = game.validate_move(moves)

        if not is_valid:
            print(errors)
            raise ValueError('Somthing Wrong')

        game.move_to(moves)

        board.grid = game.grid
        board.queue = board.players.filter(~Q(boards_players__player=user)).first()
        board.save()

        # Create new history entity
        # ...

        return board

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def update_board_in_game(self, guid: strawberry.ID, grid_changes: List[List[int]]) -> JSON:
        return update_board(guid=guid, grid_changes=grid_changes)
