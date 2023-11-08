import pprint
from typing import List
from . import models


class GamePhase:
    def __init__(self,
                 grid: List[List[int]],
                 player_queue: models.BoardPlayers,
                 move_type: int
                 ):
        self.grid = grid
        self.player_queue = player_queue
        self.move_type = move_type
        self.from_point = self.to_point = self.result = None
        self.taken_points = []

    def move_single(self):
        y1, x1 = self.from_point
        y2, x2 = self.to_point
        self.grid[y2][x2] = self.grid[y1][x1]
        self.grid[y1][x1] = 1
        self.result = self.to_point

    def move_eat(self, enemy_type):
        y1, x1 = self.from_point
        y2, x2 = self.to_point
        mid_y = (y1 + y2) // 2
        mid_x = (x1 + x2) // 2
        if abs(self.grid[mid_y][mid_x]) == enemy_type and self.grid[y2][x2] == 1:
            self.grid[y2][x2] = self.grid[y1][x1]
            self.grid[y1][x1] = 1
            self.grid[mid_y][mid_x] = 1
            self.result = self.to_point
            self.taken_points.append([mid_y, mid_x])

    def damka_move(self):
        y1, x1 = self.from_point
        y2, x2 = self.to_point
        if abs(x2 - x1) != abs(y2 - y1):
            self.result = False
            return
        dif_y = 1 if y1 < y2 else -1
        dif_x = 1 if x1 < x2 else -1

        temp_x = x1 + dif_x
        temp_y = y1 + dif_y

        enemy_count = 0
        # every square in move
        while temp_x != x2:
            current_stone = self.grid[temp_y][temp_x]
            current_square_type = self.player_queue.stone_type != abs(current_stone) and current_stone == 1
            # check
            if self.player_queue.stone_type != abs(current_stone):
                # check eat or not
                if self.player_queue.stone_type % 2 != current_stone % 2 and current_stone != 1:
                    self.grid[temp_y][temp_x] = 1
                    enemy_count += 1
                    self.taken_points.append([temp_y, temp_x])
                    if enemy_count < 2:
                        self.grid[temp_y][temp_x] = 1
                    else:
                        self.result = False
                        return

            temp_y += dif_y
            temp_x += dif_x
        # change grid
        self.grid[y2][x2] = self.grid[y1][x1]
        self.grid[y1][x1] = 1
        self.result = self.to_point
