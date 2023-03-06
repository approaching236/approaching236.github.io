import itertools
import random
import sys


SOLUTIONS = {1: 0}

sys.setrecursionlimit(2000)

def debug(f):
    actions = 0
    branches = ''

    if f in SOLUTIONS:
        return SOLUTIONS[f], ''
    elif f % 2 == 0:
        n = 1
        while f % (2**(n+1)) == 0:
            n += 1
        f /= 2**n
        actions += n
        branches += ''.join(list(itertools.repeat('D', n)))
        # print('calling solution(%s)' % f)

        odd_actions, odd_branches = solution(f)

        SOLUTIONS[f] = odd_actions
        return odd_actions + actions, branches + odd_branches
    else:
        # print('calling solution(%s)' % (f+1))
        add, add_branches = solution(f+1)
        # print('calling solution(%s)' % (f-1))
        remove, remove_branches = solution(f-1)
        if add < remove:
            branches += 'A'
            SOLUTIONS[f] = add + 1
            return add + 1, branches + add_branches
        else:
            branches += 'R'
            SOLUTIONS[f] = remove + 1
            return remove + 1, branches + remove_branches

def solution(n):
    n = int(n)

    if n in SOLUTIONS:
        return SOLUTIONS[n]
    elif n % 2 == 0:
        actions = solution(n/2) + 1

        SOLUTIONS[n] = actions
        return actions
    else:
        add = solution(n+1)
        remove = solution(n-1)

        if add < remove:
            SOLUTIONS[n] = add + 1
            return add + 1
        else:
            SOLUTIONS[n] = remove + 1
            return remove + 1

def shifty(n):
    n = int(n)
    actions = 0
    code = []

    while n != 1:
        actions += 1

        if n % 2 == 0:
            n /= 2
            code.append('D')
        else:
            pos = len(bin(n+1)) - len(bin((n+1)).rstrip('0'))
            neg = len(bin(n-1)) - len(bin((n-1)).rstrip('0'))
            if n == 3:
                actions += 1
                n = 1
            elif neg > pos:
                n -= 1
                code.append('R')
            else:
                n += 1
                code.append('A')

    print(code)
    return actions



for n in range(1, 12):

    werk = '%s ' % n
    actions = shifty(n)
    print('%s = %s' % (n, actions))

    # for a in branches:
        # if a == 'A':
            # n += 1
            # werk += 'A %s ' % n
        # elif a == 'R':
            # n -= 1
            # werk += 'R %s ' % n
        # elif a == 'D':
            # n /= 2
            # werk += 'D %s ' % n

    print(werk)
    print('')

for n in range(0, 1000):
    num_string = []
    for i in range(0, 310):
        num_string += random.choice(['6', '7', '8', '9'])

    print(solution(int(''.join(num_string))))
