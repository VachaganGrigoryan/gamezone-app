import pprint


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
    for y, row in enumerate(grid):
        for x, stone in enumerate(row):
            if abs(grid[y][x]) == stone_type:
                for o in operations:
                    temp_y = y + o[0] * 2
                    temp_x = x + o[1] * 2
                    while in_board(temp_y, temp_x, length):
                        mid_y = temp_y - o[0]
                        mid_x = temp_x - o[1]
                        if abs(grid[mid_y][mid_x]) == turns(stone_type) and grid[temp_y][temp_x] == 1:
                            if [y, x] not in from_points:
                                from_points.append([y, x])
                        if grid[y][x] > 1:
                            break
                        temp_y = temp_y + o[0]
                        temp_x = temp_x + o[1]
    return from_points


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
