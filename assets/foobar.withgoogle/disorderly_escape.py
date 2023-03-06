
'''
Normally I'd rather not include commented code, but this is a partial solution, so I'm including some to show intention
'''


def digits_in_base(i, width, b):
    assert i < b**width
    assert i >= 0
    digits = []

    for digit in range(0, width):
        digits.append(int(i % b))
        i /= b

    return digits


def enumerate_space(w, h, b):
    matrixes = []
    length = w*h

    for i in range(0, b**length):
        unraveled = digits_in_base(i, length, b)
        matrixes.append([unraveled[i:i+h] for i in range(0, w*h, h)])

    return matrixes


def group_id(matrix, b):
    row_sigs = []
    for row in matrix:
        hist = [0 for _ in range(0, b)]

        for el in row:
            hist[el] += 1

        row_sigs.append(hist)

    col_sigs = []
    for i in range(0, len(matrix[0])):
        hist = [0 for _ in range(0, b)]

        for row in matrix:
            hist[row[i]] += 1

        col_sigs.append(hist)

    
    return (sorted(row_sigs), sorted(col_sigs))


def group_to_s(group):
    dims = []
    for dim in group:
        row = []
        for hist in dim:
            row.append(','.join([str(el) for el in hist]))
            # row.append(str(int(''.join([str(el) for el in hist]), b)))
        dims.append(':'.join(row))
    return '|'.join(dims)


def mat_to_s(matrix):
    rows = []
    for row in matrix:
        rows.append(','.join([str(el) for el in row]))
    return '|'.join(rows)


def mat_to_regex_id(matrix, b):
    hist = {}
    for row in matrix:
        for el in row:
            if el not in hist:
                hist[el] = 0
            hist[el] += 1
    inversion = reversed(sorted([(hist[symbol], symbol) for symbol in hist]))
    letter_mapping = [symbol for _, symbol in inversion]

    regex = []
    for row in matrix:
        regex_row = []
        for el in row:
            regex_row.append(letter_mapping.index(el))
        regex.append(regex_row)

    return group_id(regex, b)


def solution(h, w, b):
    matrixes = enumerate_space(h, w, b)
    # print('num in space', len(matrixes))

    regexes = {}
    # symbols that are generated look like multisets
    # x_symbols = [set() for _ in range(0, h)]
    # y_symbols = [set() for _ in range(0, w)]
    for matrix in matrixes:
        group = group_id(matrix, b)
        group_str = group_to_s(group)

        regex_id = mat_to_regex_id(matrix, b)
        regex_str = group_to_s(regex_id)

        # for i, sym in enumerate(regex_id[0]):
            # x_symbols[i].add(','.join([str(el) for el in sym]))
        # for i, sym in enumerate(regex_id[1]):
            # y_symbols[i].add(','.join([str(el) for el in sym]))

        if regex_str not in regexes:
            regexes[regex_str] = {}

        if group_str not in regexes[regex_str]:
            regexes[regex_str][group_str] = []

        regexes[regex_str][group_str].append(matrix)

    calc = [{} for _ in range(0, b)]
    for regex in sorted(regexes):
        # print(regex + ' ' + str(len(regexes[regex])))
        for group in sorted(regexes[regex]):
            # print('\t'+group+' '+str(len(regexes[regex][group])))
            symbols = set()
            for mat in sorted(regexes[regex][group]):
                for row in mat:
                    for el in row:
                        symbols.add(el)
                # print('\t\t'+mat_to_s(mat))

            # if (len(regexes[regex]), len(regexes[regex][group])) not in calc[len(symbols)-1]:
            if regex not in calc[len(symbols)-1]:
                # calc[len(symbols)-1][(len(regexes[regex]), len(regexes[regex][group]))] = 0
                calc[len(symbols)-1][regex] = 0

            # calc[len(symbols)-1][(len(regexes[regex]), len(regexes[regex][group]))] += 1
            calc[len(symbols)-1][regex] += 1

    groups = 0
    for sym_count in calc:
        # These are the 'names' of the types and their group counts
        # They're organized this way to help find a closed form solution
        # print(sym_count)
        for regex in sym_count:
            groups += sym_count[regex]
    return groups


'''
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']

# cannot consistently go from given group_id to a regex pattern without swapping / resetting
def group_to_regex(group):
    h = len(group[0])
    w = len(group[1])
    b = len(group[0][0])
    symbol_mapping = []
    regex = [[None for _ in range(0, w)] for _ in range(0, h)]

    for i in range(0, h):
        for j in range(0, w):
            for k in range(0, b):
                if group[0][i][k] > 0 and group[1][j][k] > 0:
                    if k not in symbol_mapping:
                        symbol_mapping.append(k)

                    group[0][i][k] -= 1
                    group[1][j][k] -= 1 

                    regex[i][j] = LETTERS[symbol_mapping.index(k)]

                    break

    if None in regex[0] or None in regex[1]:
        return None

    return regex


regexes = {}
for group in sorted(group_to_matrixes):
    min_regex = '|'.join(mat_to_regex(min(group_to_matrixes[group])))
    max_regex = '|'.join(mat_to_regex(max(group_to_matrixes[group])))

    regex = min(min_regex, max_regex)

    if regex not in regexes:
        regexes[regex] = []

    regexes[regex].append((group, len(group_to_matrixes[group]), group_to_matrixes[group]))

groups_per_regex = {}
print('')
for regex in sorted(regexes):
    count = len(regexes[regex])
    if count not in groups_per_regex:
        groups_per_regex[count] = []
    groups_per_regex[count].append(regex)
    print(regex, len(regexes[regex]))

symbol_counts = {}
for regex in regexes:
    i = 0
    while LETTERS[i] in regex:
        i += 1

    if i not in symbol_counts:
        symbol_counts[i] = []

    symbol_counts[i].append((regex, regexes[regex]))

for n_symbols in sorted(symbol_counts):
    print(n_symbols)
    for regex, summary in symbol_counts[n_symbols]:
        print(regex, sum([group[1] for group in summary]), sorted([group[0] for group in summary]))
    print('')

print('')
regex_counts = {}
group_to_regexes = {}
mat_to_regexes = {}
for regex in sorted(regexes):
    group_count = len(regexes[regex])
    if group_count not in regex_counts:
        regex_counts[group_count] = []
    regex_counts[group_count].append(regex)
    # print('%s: %s' % (regex, group_count))
    for summary in regexes[regex]:
        if summary[0] not in group_to_regexes:
            group_to_regexes[summary[0]] = []
        group_to_regexes[summary[0]].append(regex)
        for mat in summary[2]:
            mat_str = ''
            for row in mat:
                for col in row:
                    mat_str += str(col)
            if mat_str not in mat_to_regexes:
                mat_to_regexes[mat_str] = []
            mat_to_regexes[mat_str].append(regex)
        mat_to_regexes

for group in sorted(group_to_regexes):
    print(group, group_to_regexes[group])

for mat in sorted(mat_to_regexes):
    pass
    # print(mat, mat_to_regexes[mat])

print(len(regexes))
print('')
print(len(regex_counts))
print('groups, regexes, product')
for regex_count in sorted(regex_counts):
    print("%s, %s" % (regex_count, len(regex_counts[regex_count])))
    # for regex in sorted(regex_counts[regex_count]):
        # print(regex)

print("groups: %s" % sum([regex_count * len(regex_counts[regex_count]) for regex_count in regex_counts]))

# for string in reversed(sorted(group_strings)):
    # print(string)
# print(len(group_strings))
# print('')

# x_symbols = set()
# y_symbols = set()
# for symbol in sorted(x_symbols):
    # print(symbol)
# print(len(x_symbols))
# print('')
# for symbol in sorted(y_symbols):
    # print(symbol)
# print(len(y_symbols))
'''
