import pprint

from games.checkers.GamePhase import GamePhase


def init_board(length):
    if length not in [8, 10]:
        return False

    l_middle = length // 2

    def get_num(i, j):
        if (i + j) % 2 == 0:
            return 0
        if i < l_middle - 1:
            return 2
        if i <= l_middle:
            return 1
        return 3

    return [[get_num(i, j) for j in range(length)] for i in range(length)]


def check_type(i: int, j: int, length: int):
    return -1 < i < length and -1 < j < length


def turns(stone_type):
    return 2 if stone_type == 3 else 3


def in_board(y, x, length):
    return 0 <= y < length and 0 <= x < length


def get_captureable_stones(grid, stone_type):
    length = len(grid)
    operations = [
        [1, 1],
        [-1, -1],
        [1, -1],
        [-1, 1],
    ]
    from_points = []
    to_points = []
    for y, row in enumerate(grid):
        for x, stone in enumerate(row):
            if abs(grid[y][x]) == stone_type:
                for o in operations:
                    temp_y = y + o[0] * 2
                    temp_x = x + o[1] * 2
                    while in_board(temp_y, temp_x, length):
                        mid_y = temp_y - o[0]
                        mid_x = temp_x - o[1]
                        if abs(grid[temp_y][temp_x]) == stone_type:
                            break
                        if abs(grid[mid_y][mid_x]) == turns(stone_type) and grid[temp_y][temp_x] == 1:
                            if [y, x] not in from_points:
                                from_points.append([y, x])
                            to_points.append([temp_y, temp_x])
                        if grid[y][x] > 1:
                            break
                        temp_y = temp_y + o[0]
                        temp_x = temp_x + o[1]
    return from_points, to_points


def clear(game_phase: GamePhase):
    game_phase.result = None
    game_phase.taken_points = []


def move_validation(from_point, to_point, game_phase: GamePhase):
    clear(game_phase)
    game_phase.from_point = from_point
    game_phase.to_point = to_point
    res = None
    x1, y1 = from_point
    x2, y2 = to_point
    # check what has just moved player_queue
    if game_phase.player_queue.stone_type % 2 != game_phase.grid[x1][y1] % 2:
        game_phase.result = False
    # check move direction and damka
    if game_phase.grid[x1][y1] > 0:
        if game_phase.player_queue.stone_type == 2:
            if x2 < x1 and x1 - x2 != 2:
                game_phase.result = False
        else:
            if x2 > x1 and x1 - x2 != 2:
                game_phase.result = False
    # check move destination
    if game_phase.grid[x2][y2] == 0 or game_phase.grid[x2][y2] != 1:
        game_phase.result = False
    # check simple move
    if abs(x2 - x1) == abs(y2 - y1) == 1:
        if game_phase.move_type != 1:
            game_phase.result = False
        else:
            eat_list = get_captureable_stones(game_phase.grid, game_phase.player_queue.stone_type)
            if eat_list[0]:
                res = eat_list[0]
                game_phase.result = False
            else:
                game_phase.move_single()

    # check eat move and destroy eaten stone
    elif abs(x2 - x1) == abs(y2 - y1) == 2 and game_phase.grid[x1][y1] > 1:
        if game_phase.move_type == 1:
            game_phase.result = False
        else:
            game_phase.move_eat(turns(game_phase.player_queue.stone_type))

    else:
        eat_list = get_captureable_stones(game_phase.grid, game_phase.player_queue.stone_type)
        # to_points ??
        if eat_list[0] and from_point not in eat_list[0]: # and to_point not in eat_list[1]:
            res = eat_list
            game_phase.result = False
        else:
            game_phase.damka_move()
    return {
        'grid': game_phase.grid,
        'taken_points': game_phase.taken_points,
        'res': res,
        'result': game_phase.result,
    }


if __name__ == '__main__':
    grid = [
        [
            0,
            2,
            0,
            2,
            0,
            2,
            0,
            2,
            0,
            2
        ],
        [
            1,
            0,
            2,
            0,
            2,
            0,
            2,
            0,
            2,
            0
        ],
        [
            0,
            2,
            0,
            2,
            0,
            2,
            0,
            1,
            0,
            2
        ],
        [
            2,
            0,
            2,
            0,
            2,
            0,
            2,
            0,
            2,
            0
        ],
        [
            0,
            1,
            0,
            1,
            0,
            3,
            0,
            -2,
            0,
            1
        ],
        [
            3,
            0,
            1,
            0,
            1,
            0,
            1,
            0,
            3,
            0
        ],
        [
            0,
            3,
            0,
            2,
            0,
            3,
            0,
            3,
            0,
            1
        ],
        [
            3,
            0,
            1,
            0,
            1,
            0,
            3,
            0,
            3,
            0
        ],
        [
            0,
            3,
            0,
            1,
            0,
            -3,
            0,
            3,
            0,
            3
        ],
        [
            3,
            0,
            3,
            0,
            3,
            0,
            3,
            0,
            3,
            0
        ]
    ]
    get_captureable_stones(grid, 3)
    pprint.pprint(grid)
    # pprint.pprint(init_board(8))
