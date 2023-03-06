import math


def cells_lit((rx, ry), (x0, y0), (x1, y1)):
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
    # zero up
    elif y0 < y1:
        wall = 0.0
        while (wall*ry) < y1:
            x = ((wall*ry - y0)*(x1 - x0))/(y1 - y0) + x0

            cx = math.floor(x/rx)

            cells.add((cx, wall+1))
            cells.add((cx, wall))
            wall += 1

    # neg one down
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

    x_actual = rx * cx + x_local
    y_actual = ry * cy + y_local

    return (x_actual, y_actual)


def is_between((sx, sy), (mx, my), (tx, ty)):
    if sx >= mx and mx >= tx and sy <= my and my <= ty:
        return True
    elif sx <= mx and mx <= tx and sy <= my and my <= ty:
        return True
    elif sx >= mx and mx >= tx and sy >= my and mx >= ty:
        return True
    elif sx <= mx and mx <= tx and sy >= my and my >= ty:
        return True

    return False


# checks to see if (mx, my) is on line defined by points (x0, y0) and (x1, y1)
def is_colinear((x0, y0), (mx, my), (x1, y1)):
    if x0 == mx and mx == x1:
        return True
    elif y0 == my and my == y1:
        return True
    elif x0 == x1 and x0 != mx:
        return False
    else:
        return my == ((float((mx - x0)*(y1 - y0))/float(x1 - x0)) + y0)


def is_obstructed((rx, ry), (sx, sy), (cx, cy), (tx, ty)):
    x0, y0 = xy_actual((rx, ry), (0, 0), (sx, sy))
    x1, y1 = xy_actual((rx, ry), (cx, cy), (tx, ty))

    if (cx, cy) == (0, 0):
        return False

    for cell in cells_lit((rx, ry), (x0, y0), (x1, y1)):
        # source / target of cell being checked
        sxa, sya = xy_actual((rx, ry), cell, (sx, sy))
        txa, tya = xy_actual((rx, ry), cell, (tx, ty))

        source_reflected_colinear = is_colinear((x0, y0), (sxa, sya), (x1, y1))
        target_reflected_colinear = is_colinear((x0, y0), (txa, tya), (x1, y1))
        source_between = is_between((x0, y0), (sxa, sya), (x1, y1))
        target_between = is_between((x0, y0), (txa, tya), (x1, y1))

        if cell == (0, 0):
            if target_between and target_reflected_colinear:
                return True
        elif cell == (cx, cy):
            if (sxa, sya) != (x1, y1) and source_between and source_reflected_colinear:
                return True
        else:
            if source_between and source_reflected_colinear:
                return True
            if target_between and target_reflected_colinear:
                return True

    return False


def solution((rx, ry), (sx, sy), (tx, ty), d):
    x_bound = int(math.ceil(float(d) / rx))
    y_bound = int(math.ceil(float(d) / ry))

    count = 0

    # scan square, only check in jagged circle (distance < d)
    for cx in range(-x_bound, x_bound):
        for cy in range(-y_bound, y_bound):
            x0, y0 = xy_actual((rx, ry), (0, 0), (sx, sy))
            x1, y1 = xy_actual((rx, ry), (cx, cy), (tx, ty))

            match_distance = math.sqrt(float(abs(x0 - x1)**2 + abs(y0 - y1)**2))

            if match_distance <= d and not is_obstructed((rx, ry), (sx, sy), (cx, cy), (tx, ty)):
                count += 1

    return count
