
def digits_in_base(i, k, b):
    assert i < b**k
    assert i >= 0
    digits = []

    for digit in range(0, k):
        digits.append(int(i % b))
        i //= b

    return digits[::-1]


def next_num(i, k, b):
    digits = digits_in_base(i, k, b)

    big = sum([p*b**(k-i-1) for (i, p) in enumerate(sorted(digits, reverse=True))])
    small = sum([p*b**(k-i-1) for (i, p) in enumerate(sorted(digits))])

    # print(f"{i}, {digits} => {list(sorted(digits, reverse=True))} - {list(sorted(digits))} = {big}\t - {small}\t = {big - small}")

    return big - small
    

def enumerate_base(k, b):
    subgroups = {}
    results_for_base = []

    for i in range(0, b**k):
        difference = next_num(i, k, b)

        results_for_base.append(difference)
        if difference in subgroups:
            subgroups[difference].append(i)
        else:
            subgroups[difference] = [i]

    #!! results always symetric
    # print(results_for_base == list(reversed(results_for_base)))
    print(f"subgroups: {len(subgroups)}")
    print(sorted(subgroups.keys()))
    # print(subgroups)

def traverse(digit_str, b):
    results = []
    k = len(digit_str)
    current = sum([int(p)*b**(k-i-1) for (i, p) in enumerate(digit_str)])

    while current not in results:
        results.append(current)
        current = next_num(current, k, b)

    return len(results) - results.index(current)

# print(digits_in_base(13, 5, 3))
# print(list(reversed(digits_in_base(3, 4, 3))))

# for k in range(2, 10):
    # for base in range(6, 10):
        # print()
        # print(f"k: {k} base: {base}")
        # enumerate_base(k, base)
       

traverse('210022', 3)
traverse('1211', 10)
# assert solution('210022', 3) == 3
# assert solution('1211', 10) == 3
