from datetime import datetime
from typing import List, Tuple

import strawberry

from core.json import JSON
from . import models
from .GamePhase import GamePhase
from .models import BoardPlayers, Histories
import enum
from .utils import get_captureable_stones, move_validation, looser


class CC(enum.Enum):
    White = 'White'
    Black = 'Black'


class Game:

    def __init__(self, grid: List[List[int]], player_stone: int):
        self.grid = grid
        self.player_stone = player_stone

    def validate_move(self, moves: List[List[int]]) -> Tuple[bool, List]:
        errors = []
        if len(moves) == 2:
            if self.have_eats_move():
                errors.append({
                    'type': 'incorrect-have-eats',
                    'message': 'You need to eat stone.'
                })
            elif not self.can_move(moves):
                errors.append({
                    'type': 'incorrect-move',
                    'message': 'You cant do move.'
                })
        elif len(moves) > 2:
            if not self.can_eat(moves):
                errors.append({
                    'type': 'incorrect-eat-or-move',
                    'message': 'You can not eat stone.'
                })
        else:
            errors.append({
                'type': 'incorrect-move',
                'message': 'Moves is incorrect.'
            })

        return len(errors) == 0, errors

    def have_eats_move(self) -> bool:
        ...

    def can_eat(self, moves) -> bool:
        ...

    def can_move(self, moves) -> bool:
        ...

    def move_to(self, moves):
        ...

    def is_ended(self) -> bool:
        ...


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

    for i in range(len(grid_changes) - 1):
        from_point = grid_changes[i]
        to_point = grid_changes[i + 1]
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
    if not game_phase.result and (not moves_result or
                                  (moves_result in eat_list[0] and taken_points)):
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
        # determine winner
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
