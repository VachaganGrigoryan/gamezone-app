import pprint
from datetime import datetime
from functools import reduce
from typing import List

import strawberry
from asgiref.sync import sync_to_async

from core.json import JSON
from . import models
from .models import Board, BoardPlayers, Histories
import enum
from .utils import init_board
from account.models import User


class CC(enum.Enum):
    White = 'White'
    Black = 'Black'


@sync_to_async
def init_game(guid, color=CC.White.value, length=8):
    owner = User.objects.get(guid=guid)
    if not owner:
        return 'no user'
    board = Board.objects.create(
        owner=owner,
        queue=owner if color == CC.White.value else None,
        grid=init_board(length),
    )
    BoardPlayers.objects.create(
        board=board,
        player=owner,
        stone_type=2 if color == CC.White.value else 3
    )

    temp = {"guid": str(board.guid), "board": list(board.grid)}
    return temp


@sync_to_async
def update_board(
        guid: strawberry.ID,
        grid_changes: List[List[int]]
) -> JSON:
    board = models.Board.objects.get(guid=guid)
    player_queue = BoardPlayers.objects.get(player=board.queue)
    taken_points = []
    # message for developer
    message = 'everything is ok'

    # function for reduce
    def move_validation(from_point, to_point):
        if not from_point:
            return False
        x1, y1 = from_point
        x2, y2 = to_point

        # check what has just moved player_queue
        if player_queue.stone_type % 2 != board.grid[x1][y1] % 2:
            return False
        # check move direction and damka
        if board.grid[x1][y1] < 3:
            if player_queue.stone_type == 2:
                if x2 < x1 and x1 - x2 != 2:
                    return False
            else:
                if x2 > x1 and x1 - x2 != 2:
                    return False
        # check move destination
        if board.grid[x2][y2] == 0 or board.grid[x2][y2] != 1:
            return False
        # check simple move
        if abs(x2 - x1) == abs(y2 - y1) == 1:
            board.grid[x2][y2] = board.grid[x1][y1]
            board.grid[x1][y1] = 1
            return to_point
        # check eat move and destroy eaten stone
        if abs(x2 - x1) == abs(y2 - y1) == 2 and board.grid[x1][y1] < 4:
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            if board.grid[mid_x][mid_y] == board.grid[x1][y1]:
                print(False)
                return False
            board.grid[x2][y2] = board.grid[x1][y1]
            board.grid[x1][y1] = 1
            board.grid[mid_x][mid_y] = 1
            taken_points.append([mid_x, mid_y])
            return to_point

        # already damka
        # check diagonal
        if abs(x2 - x1) != abs(y2 - y1):
            return {'error': 'not diagonal'}
        dif_x = 1 if x1 < x2 else -1
        dif_y = 1 if y1 < y2 else -1

        temp_x = x1 + dif_x
        temp_y = y1 + dif_y

        enemy_count = 0
        # every square in move
        while temp_x != x2:
            current_stone = board.grid[temp_x][temp_y]
            current_stone_type = player_queue.stone_type % 2 == current_stone % 2 and current_stone != 1
            # check
            if current_stone_type:
                return False
            else:
                # check eat or not
                if player_queue.stone_type % 2 != current_stone % 2 and current_stone != 1:
                    board.grid[temp_x][temp_y] = 1
                    enemy_count += 1
                    taken_points.append([temp_x, temp_y])
                if enemy_count < 2:
                    board.grid[temp_x][temp_y] = 1
                else:
                    return False

            temp_x += dif_x
            temp_y += dif_y
        # change grid
        board.grid[x2][y2] = board.grid[x1][y1]
        board.grid[x1][y1] = 1
        return to_point

    # calling validation function
    last_move = reduce(lambda from_point, to_point: move_validation(from_point, to_point), grid_changes)

    # check function result
    if last_move != grid_changes[-1]:
        message = 'Wrong move'
    else:
        # check damka
        if player_queue.stone_type == 2 and last_move[0] == 7:
            board.grid[last_move[0]][last_move[1]] = 4
        if player_queue.stone_type == 3 and last_move[0] == 0:
            board.grid[last_move[0]][last_move[1]] = 5
        # everything is ok
        # save changes
        now = datetime.now()
        Histories.objects.create(
            board=board,
            player=player_queue.player,
            from_point=grid_changes[0],
            to_points=grid_changes[1:],
            taken_points=taken_points,
            played_at=now,
        )
        board.queue = board.get_next_queue(board.queue)
        board.updated_at = now
        board.save()
    return {
        "queue": str(board.queue),
        "grid": board.grid,
        "updated_at": str(board.updated_at),
        "message": message,
    }
