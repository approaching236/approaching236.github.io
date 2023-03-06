import math
from fractions import Fraction
import time


ACTUAL_COORDS = {}
OBSTRUCTED_SLOPES = {}

CALLS = {
        'cells_lit': 0,
        'xy_actual': 0,
        'between': 0,
        'colinear': 0,
        'colinear_a': 0,
        'colinear_b': 0,
        'colinear_c': 0,
        'colinear_d': 0,
        'distance': 0,
        'add_obstruction': 0,
        'obstructed': 0,
        'cached_obstruction_between': 0,
        }


def cells_lit((rx, ry), (x0, y0), (x1, y1)):
    CALLS['cells_lit'] += 1
    cells = set()

    # x crossings
    if x0 == x1:
        pass
    elif x0 < x1:
        wall = 1.0
        while (wall*rx) <= x1:
            y = ((wall*rx - x0)*(y1 - y0))/(x1-x0) + y0

            cy = math.ceil(y/ry)

            cells.add((wall-1, cy))
            cells.add((wall, cy))
            wall += 1
    else:
        wall = 0.0
        while (wall*rx) > x1:
            y = ((wall*rx - x0)*(y1 - y0))/(x1-x0) + y0

            cy = math.ceil(y/ry)

            cells.add((wall-1, cy))
            cells.add((wall, cy))
            wall -= 1

    # y crossings
    if y0 == y1:
        pass
    elif y0 < y1:
        wall = 0.0
        while (wall*ry) < y1:
            x = ((wall*ry - y0)*(x1 - x0))/(y1 - y0) + x0

            cx = math.floor(x/rx)

            cells.add((cx, wall+1))
            cells.add((cx, wall))
            wall += 1

    else:
        wall = -1.0

        while (wall*ry) > y1:
            x = ((wall*ry - y0)*(x1 - x0))/(y1 - y0) + x0

            cx = math.floor(x/rx)

            cells.add((cx, wall+1))
            cells.add((cx, wall))
            wall -= 1

    return cells


def xy_actual((rx, ry), (cx, cy), (x, y)):
    CALLS['xy_actual'] += 1
    if (rx, ry, cx, cy, x, y) in ACTUAL_COORDS:
        return ACTUAL_COORDS[(rx, ry, cx, cy, x, y)]

    x_local, y_local = None, None

    if cx % 2 == 0 and cy % 2 == 0:
        x_local = x
        y_local = -y
    elif cx % 2 == 0 and cy % 2 == 1:
        x_local = x
        y_local = -(ry - y)
    elif cx % 2 == 1 and cy % 2 == 0:
        x_local = rx - x
        y_local = -y
    else:
        x_local = rx - x
        y_local = -(ry - y)

    x_actual = int(rx * cx + x_local)
    y_actual = int(ry * cy + y_local)

    
    ACTUAL_COORDS[(rx, ry, cx, cy, x, y)] = (x_actual, y_actual)
    return (x_actual, y_actual)


def between((sx, sy), (mx, my), (tx, ty)):
    CALLS['between'] += 1
    if sx >= mx and mx >= tx and sy <= my and my <= ty:
        return True
    elif sx <= mx and mx <= tx and sy <= my and my <= ty:
        return True
    elif sx >= mx and mx >= tx and sy >= my and my >= ty:
        return True
    elif sx <= mx and mx <= tx and sy >= my and my >= ty:
        return True

    return False


# checks to see if (mx, my) is on line defined by points (x0, y0) and (x1, y1)
def colinear((x0, y0), (mx, my), (x1, y1)):
    CALLS['colinear'] += 1
    if x0 == mx and mx == x1:
        return True
    elif y0 == my and my == y1:
        return True
    elif x0 == x1 and x0 != mx:
        return False
    else:
        return my == ((float((mx - x0)*(y1 - y0))/float(x1 - x0)) + y0)


def add_obstruction((sxa, sya), (obxa, obya)):
    CALLS['add_obstruction']
    slope = None
    if sxa == obxa:
        slope = 'inf'
    else:
        slope = Fraction(obya - sya, obxa - sxa)

    if slope not in OBSTRUCTED_SLOPES:
        OBSTRUCTED_SLOPES[slope] = []

    OBSTRUCTED_SLOPES[slope].append((obxa, obya))


def cached_obstruction_between((sxa, sya), (txa, tya)):
    CALLS['cached_obstruction_between']
    slope = None
    if sxa == txa:
        slope = 'inf'
    else:
        slope = Fraction(tya - sya, txa - sxa)

    if slope in OBSTRUCTED_SLOPES:
        for obstruction in OBSTRUCTED_SLOPES[slope]:
            if obstruction != (txa, tya) and between((sxa, sya), obstruction, (txa, tya)):
                return True

    return False


def obstructed((rx, ry), (sx, sy), (cx, cy), (tx, ty)):
    CALLS['obstructed'] += 1
    x0, y0 = xy_actual((rx, ry), (0, 0), (sx, sy))
    x1, y1 = xy_actual((rx, ry), (cx, cy), (tx, ty))

    if cached_obstruction_between((x0, y0), (x1, y1)):
        return True

    if (cx, cy) == (0, 0):
        return False

    for cell in cells_lit((rx, ry), (x0, y0), (x1, y1)):
        # source / target of cell being checked
        sxa, sya = xy_actual((rx, ry), cell, (sx, sy))
        txa, tya = xy_actual((rx, ry), cell, (tx, ty))

        # origin cell
        if cell == (0, 0):
            CALLS['colinear_a'] += 1
            if colinear((x0, y0), (txa, tya), (x1, y1)) and between((x0, y0), (txa, tya), (x1, y1)):
                add_obstruction((x0, y0), (txa, tya))
                return True
        # target cell
        elif cell == (cx, cy):
            CALLS['colinear_b'] += 1
            if (sxa, sya) != (x1, y1) and colinear((x0, y0), (sxa, sya), (x1, y1)) and between((x0, y0), (sxa, sya), (x1, y1)):
                add_obstruction((x0, y0), (sxa, sya))
                return True
        # middle cell
        else:
            CALLS['colinear_c'] += 1
            if colinear((x0, y0), (sxa, sya), (x1, y1)) and between((x0, y0), (sxa, sya), (x1, y1)):
                add_obstruction((x0, y0), (sxa, sya))
                return True
            CALLS['colinear_d'] += 1
            if colinear((x0, y0), (txa, tya), (x1, y1)) and between((x0, y0), (txa, tya), (x1, y1)):
                add_obstruction((x0, y0), (txa, tya))
                return True

    add_obstruction((x0, y0), (x1, y1))

    return False


def distance((rx, ry), (sx, sy), (cx, cy), (tx, ty)):
    CALLS['distance'] += 1
    x0, y0 = xy_actual((rx, ry), (0, 0), (sx, sy))
    x1, y1 = xy_actual((rx, ry), (cx, cy), (tx, ty))

    return math.sqrt(float(abs(x0 - x1)**2 + abs(y0 - y1)**2))


def solution(room_dim, source, target, d):
    # scan inside out, warmer cache, less corner loss
    count = 0
    # Quadrant A
    (cx, cy) = (0, 0)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            if not obstructed(room_dim, source, (cx, cy), target):
                # print('A', cx, cy)
                count += 1
            cx += 1
        cx = 0
        cy += 1
    # Quandrant B
    (cx, cy) = (-1, 0)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            if not obstructed(room_dim, source, (cx, cy), target):
                # print('B', cx, cy)
                count += 1
            cy += 1
        cy = 0
        cx -= 1
    # Quadrant C
    (cx, cy) = (-1, -1)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            if not obstructed(room_dim, source, (cx, cy), target):
                # print('C', cx, cy)
                count += 1
            cy -= 1
        cy = -1
        cx -= 1
    # Quadrant D
    (cx, cy) = (0, -1)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            if not obstructed(room_dim, source, (cx, cy), target):
                # print('D', cx, cy)
                count += 1
            cx += 1
        cx = 0
        cy -= 1

    print(CALLS)
    return count


# print(solution((3, 2), (1, 1), (2, 1), 4), 7)
# print(solution((2, 3), (1, 1), (1, 2), 4), 7)
start = time.time()
# print(solution([300,275], [150,150], [185,100], 500), 9)
print(solution([5, 3], [2, 2], [4, 1], 200))
print(time.time() - start)
