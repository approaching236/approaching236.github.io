import math
from fractions import Fraction


ACTUAL_COORDS = {}
OBSTRUCTED_SLOPES = {}


def xy_actual((rx, ry), (cx, cy), (x, y)):
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
    if sx >= mx and mx >= tx and sy <= my and my <= ty:
        return True
    elif sx <= mx and mx <= tx and sy <= my and my <= ty:
        return True
    elif sx >= mx and mx >= tx and sy >= my and my >= ty:
        return True
    elif sx <= mx and mx <= tx and sy >= my and my >= ty:
        return True

    return False


def add_obstruction(room_dim, source, target_cell, target):

    if source == target and target_cell == (0, 0):
        return False

    x0, y0 = xy_actual(room_dim, (0, 0), source)
    x1, y1 = xy_actual(room_dim, target_cell, target)

    slope = None
    if x0 == x1:
        slope = 'inf'
    else:
        slope = Fraction(y1 - y0, x1 - x0)

    if slope not in OBSTRUCTED_SLOPES:
        OBSTRUCTED_SLOPES[slope] = []

    OBSTRUCTED_SLOPES[slope].append((x1, y1))


def cached_obstruction_between((sxa, sya), (txa, tya)):
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
    x0, y0 = xy_actual((rx, ry), (0, 0), (sx, sy))
    x1, y1 = xy_actual((rx, ry), (cx, cy), (tx, ty))

    if cached_obstruction_between((x0, y0), (x1, y1)):
        return True

    if (cx, cy) == (0, 0):
        return False

    return False


def distance((rx, ry), (sx, sy), (cx, cy), (tx, ty)):
    x0, y0 = xy_actual((rx, ry), (0, 0), (sx, sy))
    x1, y1 = xy_actual((rx, ry), (cx, cy), (tx, ty))

    return math.sqrt(float(abs(x0 - x1)**2 + abs(y0 - y1)**2))


def solution(room_dim, source, target, d):
    # scan inside out for less corner loss
    # start by warming cache
    # Quadrant A
    (cx, cy) = (0, 0)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            add_obstruction(room_dim, source, (cx, cy), source)
            add_obstruction(room_dim, source, (cx, cy), target)
            cx += 1
        cx = 0
        cy += 1
    # Quandrant B
    (cx, cy) = (-1, 0)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            add_obstruction(room_dim, source, (cx, cy), source)
            add_obstruction(room_dim, source, (cx, cy), target)
            cy += 1
        cy = 0
        cx -= 1
    # Quadrant C
    (cx, cy) = (-1, -1)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            add_obstruction(room_dim, source, (cx, cy), source)
            add_obstruction(room_dim, source, (cx, cy), target)
            cy -= 1
        cy = -1
        cx -= 1
    # Quadrant D
    (cx, cy) = (0, -1)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            add_obstruction(room_dim, source, (cx, cy), source)
            add_obstruction(room_dim, source, (cx, cy), target)
            cx += 1
        cx = 0
        cy -= 1

    # actually count
    count = 0
    (cx, cy) = (0, 0)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            if not obstructed(room_dim, source, (cx, cy), target):
                count += 1
            cx += 1
        cx = 0
        cy += 1
    # Quandrant B
    (cx, cy) = (-1, 0)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            if not obstructed(room_dim, source, (cx, cy), target):
                count += 1
            cy += 1
        cy = 0
        cx -= 1
    # Quadrant C
    (cx, cy) = (-1, -1)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            if not obstructed(room_dim, source, (cx, cy), target):
                count += 1
            cy -= 1
        cy = -1
        cx -= 1
    # Quadrant D
    (cx, cy) = (0, -1)
    while distance(room_dim, source, (cx, cy), target) <= d:
        while distance(room_dim, source, (cx, cy), target) <= d:
            if not obstructed(room_dim, source, (cx, cy), target):
                count += 1
            cx += 1
        cx = 0
        cy -= 1

    return count


print(solution((3, 2), (1, 1), (2, 1), 4), 7)
print(solution((2, 3), (1, 1), (1, 2), 4), 7)
start = time.time()
print(solution([300,275], [150,150], [185,100], 500), 9)
# print(solution([5, 3], [2, 2], [4, 1], 200))
print(time.time() - start)
