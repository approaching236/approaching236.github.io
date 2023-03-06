import itertools

def solution(sources, dests, adj_mat):
    print(sources, dests, adj_mat)

    dim = len(adj_mat)
    zero_row = list(itertools.repeat(0, dim))

    # deleting bottom up / outside in doesn't disturb indexes
    sources = list(reversed(sorted(sources)))
    dests = list(reversed(sorted(dests)))

    # prune paths

    for i in range(0, dim):
        # zero dest outputs
        for dest in dests:
            adj_mat[dest][i] = 0

        # zero anything to source
        for source in sources:
            adj_mat[i][source] = 0

    # remove leaf nodes
    leaves = []
    for i in range(0, dim):
        if sum(adj_mat[i]) == 0 and i not in dests:
            leaves.append(i)
            # get column i, non-zero indexes 
    while leaves:
        deprecation = leaves.pop()
        for i in range(0, dim):
            if adj_mat[i][deprecation] != 0:
                adj_mat[i][deprecation] = 0
                if sum(adj_mat[i]) == 0:
                    leaves.append(i)

    # sum all sources
    if len(sources) > 1:
        source = sources[0]
        for deprecation in sources[1:]:
            adj_mat[source] = [x+y for x, y in zip(adj_mat[source], adj_mat[deprecation])]

        # delete old rows
        old_sources = list(sources[1:])
        for deprecation in old_sources:
            adj_mat[deprecation] = zero_row

        # delete old columns
        for deprecation in old_sources:
            for room in range(0, dim):
                adj_mat[room][deprecation] = 0


    # sum all dests
    if len(dests) > 1:
        dest = dests[0]
        for deprecation in dests[1:]:
            for room in range(0, dim):
                adj_mat[room][dest] += adj_mat[room][deprecation]
                adj_mat[room][deprecation] = 0

            adj_mat[deprecation] = zero_row

    evacuated = 0
    while sum(adj_mat[source]) > 0 and sum([adj_mat[i][dest] for i in range(0, dim)]) > 0:
        path = [source]
        cursor = source
        while cursor != dest:
            outputs = [i for i, v in enumerate(adj_mat[cursor]) if v > 0 and i not in path]
            if outputs:
                cursor = outputs[0]
                path.append(cursor)
            else:
                for i in range(0, dim):
                    adj_mat[i][cursor] = 0
                break
        evac = min([adj_mat[path[i]][path[i+1]] for i in range(0, len(path)-1)])
        evacuated += evac
        updated_volumes = [adj_mat[path[i]][path[i+1]] - evac for i in range(0, len(path)-1)]
        for i in range(0, len(path)-1):
            adj_mat[path[i]][path[i+1]] = updated_volumes[i]

    return evacuated

# 'resolved' source if + -#-> - 
# sum all ^^ w/o disjoint


print('too sourcy')
print(solution([0, 1], [2], [[2, 3, 5], [4, 2, 6], [0, 0, 0]]))

print('too desty')
print(solution([0], [3, 4], [[0, 1, 2, 0, 0], [0, 0, 0, 3, 2], [0, 0, 0, 5, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]))

print('basic triangles')
print(solution([0], [2], [[0, 7, 6], [0, 0, 5], [0, 0, 0]]))
print(solution([0], [1], [[0, 6, 7], [0, 0, 0], [0, 5, 0]]))

print('join / diverge')
print(solution([0, 2], [1], [[0, 3, 0], [0, 0, 0], [0, 2, 0]]))
print(solution([0], [1, 2], [[0, 3, 4], [0, 0, 0], [0, 0, 0]]))

print('given LLL')
print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]))

print('disjoint')
print(solution([0, 2], [1, 3], [[0, 4, 0, 0], [0, 0, 0, 0], [0, 0, 5, 0], [0, 0, 0, 0]]))
print(solution([0], [1], [[0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 3], [0, 0, 3, 0]]))

print('long leaf')
print(solution([0], [4], [[0, 2, 0, 0, 0], [0, 0, 3, 0, 2], [0, 0, 0, 3, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]))


print('long diamond')
print(solution([0], [5], [[0, 5, 0, 0, 0, 0], [0, 0, 3, 4, 0, 0], [0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 6, 0], [0, 8, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0]]))

print('given big boi')
print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
