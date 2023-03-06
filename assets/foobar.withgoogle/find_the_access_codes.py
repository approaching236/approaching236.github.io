import itertools
import random
import time

def slow(l):
    lucky_tuples = []

    for (a, b, c) in itertools.combinations(l, 3):
        if (b % a) == 0 and (c % b ) == 0:
            lucky_tuples.append((a, b, c))

    return len(lucky_tuples)

def solution(l):
    triples = set()
    lucky_triple_count = 0
    n = len(l)

    for i, a in enumerate(itertools.islice(l, 0, n-2)):
        for j, b in enumerate(itertools.islice(l, i+1, n-1)):
            if (b % a) == 0:
                for c in itertools.islice(l, i+j+2, None):
                    if (c % b) == 0:
                        triple_tag = "%s,%s,%s" % (a, b, c)
                        triples.add(triple_tag)
                        lucky_triple_count += 1

    return lucky_triple_count


def solution(l):
    n = len(l)

    follow_factors = {}
    triple_count = 0
    tested = {}

    for i, s in enumerate(itertools.islice(l, 0, n-1)):
        if s in tested:
            follow_factors[i] = follow_factors[tested[s]][follow_factors[tested[s]].index(i)+1:]
        else:
            for j, t in enumerate(itertools.islice(l, i+1, None)):
                if (t % s) == 0:
                    k = i + j + 1
                    if i in follow_factors:
                        follow_factors[i].append(k)
                    else:
                        follow_factors[i] = [k]
            tested[s] = i

    for i in follow_factors.keys():
        for j in follow_factors[i]:
            if j in follow_factors:
                triple_count += len(follow_factors[j])

    return triple_count

def submitted(l):
    follow_factors = {}
    tested = {}

    # build up indexes where s|t
    for i, s in enumerate(itertools.islice(l, 0, len(l)-1)):
        if s in tested:
            # copy applicaple already scanned
            follow_factors[i] = follow_factors[tested[s]][follow_factors[tested[s]].index(i)+1:]
        else:
            for j, t in enumerate(itertools.islice(l, i+1, None)):
                if (t % s) == 0:
                    k = i + j + 1
                    if i in follow_factors:
                        follow_factors[i].append(k)
                    else:
                        follow_factors[i] = [k]
            tested[s] = i
    
    triple_count = 0
    for i in follow_factors.keys():
        for j in follow_factors[i]:
            if j in follow_factors:
                triple_count += len(follow_factors[j])

    return triple_count



print(solution([1, 2, 3, 4, 5, 6]))
print('')
print(solution([1, 1, 2, 2, 1, 1]))
print('')
print("ones:")
for num in range(2, 8):
    print(solution(list(itertools.repeat(1, num))))
    print('')
print('')
print('rangers:')
# for num in range(20, 200):
    # print(solution(list(range(1, num))))
print('')
# print("2k:")
# print(solution(list(range(1, 2000))))
print("big one:")
print(solution(list(itertools.repeat(1, 1000))))
# print(solution([1, 2, 5, 3, 4, 5, 6, 7, 8]))
# print(solution([6, 3, 2, 4, 5, 1]))
print()

start = time.time()
for i in range(0, 0):
    code_list = [int(random.uniform(1, 999999)) for i in range(0, 2000)]
    triples = solution(code_list)
    print(triples)

print(time.time() - start)
