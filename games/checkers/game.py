from datetime import datetime
from functools import reduce
from typing import List

import strawberry
from asgiref.sync import sync_to_async

from core.json import JSON
from . import models
from .GamePhase import GamePhase
from .models import Board, BoardPlayers, Histories
import enum
from .utils import init_board, get_captureable_stones, move_validation
from account.models import User


class CC(enum.Enum):
    White = 'White'
    Black = 'Black'


@sync_to_async
def init_game(guid, color=CC.White.value, length=8):
    owner = User.objects.get(guid=guid)
    if not owner:
        return 'no user'
    grid = init_board(length)
    if not grid:
        return {
            'error': "The Board should be have 8 or 10 length!"
        }
    board = Board.objects.create(
        owner=owner,
        queue=owner if color == CC.White.value else None,
        grid=grid,
    )
    BoardPlayers.objects.create(
        board=board,
        player=owner,
        stone_type=2 if color == CC.White.value else 3
    )

    return {
        "guid": str(board.guid),
        "board": board.grid
    }


@sync_to_async
def update_board(
        guid: strawberry.ID,
        grid_changes: List[List[int]]
) -> JSON:
    board = models.Board.objects.get(guid=guid)
    player_queue = BoardPlayers.objects.get(player=board.queue, board=board)
    move_type = abs(grid_changes[0][0] - grid_changes[1][0])

    game_phase = GamePhase(board.grid, player_queue, move_type)
    res = []
    taken_points = []
    moves_result = True
    # message for developer
    message = 'everything is ok'

    for i in range(len(grid_changes)-1):
        from_point = grid_changes[i]
        to_point = grid_changes[i+1]
        temp = move_validation(from_point, to_point, game_phase)
        moves_result = temp['result']
        res = temp['res']
        if not moves_result:
            break
        taken_points = temp['taken_points']
        board.grid = temp['grid']

    eat_list = get_captureable_stones(game_phase.grid, game_phase.player_queue.stone_type)
    if grid_changes[-1] in eat_list[0] and taken_points:
        res = grid_changes[-1]
        moves_result = False

    winner = None

    if (not moves_result or
            (moves_result in get_captureable_stones(board.grid, player_queue.stone_type) and taken_points)):
        message = 'Wrong move'
    else:
        # check damka
        if player_queue.stone_type == 2 and moves_result[0] == 7:
            board.grid[moves_result[0]][moves_result[1]] = -2
        if player_queue.stone_type == 3 and moves_result[0] == 0:
            board.grid[moves_result[0]][moves_result[1]] = -3
        # everything is ok
        # save changes
        now = datetime.now()
        Histories.objects.create(
            board=board,
            player=player_queue.player,
            grid_changes=grid_changes,
            taken_points=taken_points,
            played_at=now,
        )
        board.queue = board.get_next_queue(current=board.queue)
        board.updated_at = now

        winner = None
        #determine winner
        if not looser(board.grid, player_queue.stone_type):
            winner = board.get_next_queue(current=board.queue)
        board.save()

    return {
        "queue": str(board.queue),
        "grid": board.grid,
        "updated_at": str(board.updated_at),
        "res": res,
        "message": message,
        "winner": winner,
    }


@sync_to_async
def get_board(guid):
    board = models.Board.objects.get(guid=guid)
        # guid = types.CheckersBoardType.guid

    return {
    "queue": str(board.queue),
    "grid": board.grid,
    "updated_at": str(board.updated_at),
    }
