import itertools


def reproduce_asexually(m, f):
    return (m + list(itertools.repeat(0, f)), f)


def reproduce_sexually(m, f):
    for i in range(0, f):
        try:
            m[i] += 1
        except:
            pass

    return (m, f + sum(m))


def breadth(target_m, target_f):
    target_m, target_f = int(target_m), int(target_f)
    generations = [[([0], 1)]]

    for g in range(1, 5):
        # print(g)
        if g not in generations:
            generations.append([])

        for (machs, faculas) in generations[g-1]:
            generations[g].append(reproduce_asexually(machs, faculas))
            generations[g].append(reproduce_sexually(machs, faculas))

    for g in range(0, 5):
        # print(g)

        for (machs, faculas) in generations[g]:
            # print(len(machs), faculas)
            if len(machs) == target_m and faculas == target_f:
                # print("found (%s, %s) in generation: %s" % (target_m, target_f, g))
                return str(g)

    print("did not find (%s, %s) after %s generations" % (target_m, target_f, g))
    return 'impossible'

def solution(x, y):
    x, y = int(x), int(y)
    g = 0

    while x > 0 and y > 0:
        if x == 1:
            g += (y - 1)
            return str(g)
        elif y == 1:
            g += (x - 1)
            return str(g)
        elif x > y:
            multiples = x / y
            g += multiples
            x = x - (multiples * y)
        else:
            multiples = y / x
            g += multiples
            y = y - (multiples * x)

    return 'impossible'
            
print('beginning test cases:')
assert solution('2', '4') == 'impossible'
assert solution('4', '7') == '4'
assert solution('2', '1') == '1'
print('given test cases pass!')
