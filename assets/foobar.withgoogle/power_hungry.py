import itertools

from functools import reduce
from operator import mul


def solution(xs):
    biggest_product = None

    if 0 in xs:
        biggest_product = 0
        xs = list(filter(lambda a: a != 0, xs))

    pos_xs = list(filter(lambda a: a > 0, xs))
    neg_xs = list(filter(lambda a: a < 0, xs))

    for n in range(1, len(neg_xs) + 1):
        for combo in itertools.combinations(neg_xs, n):
            if biggest_product is None:
                biggest_product = reduce(mul, combo)
            else:
                current = reduce(mul, combo)
                if current > biggest_product:
                    biggest_product = current

    final_product = None
    if pos_xs:
        pos_product = reduce(mul, pos_xs, 1)

        if biggest_product <= 0:
            final_product = pos_product
        else:
            final_product = biggest_product * pos_product
    else:
        final_product = biggest_product

    return str(final_product)

print(solution([2, 0, 2, 2, 0]))
print(solution([-2, 0, -2, -2, 0]))
print(solution([-2, -3, 4, -5]))
print(solution([2, -3, 1, 0, -5]))
print(solution([-5, -5, -5, -1]))
print(solution([-5, -4, 2, 2, 2, 2, 2, 2, 2, 2,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7]))
