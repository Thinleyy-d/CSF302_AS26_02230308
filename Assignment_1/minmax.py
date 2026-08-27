import random

def minmax308(A308, count308):
    n308 = len(A308)

    # One element
    if n308 == 1:
        return A308[0], A308[0]

    # Two elements
    if n308 == 2:
        count308[0] += 1

        if A308[0] < A308[1]:
            return A308[0], A308[1]
        else:
            return A308[1], A308[0]

    # Divide
    mid308 = n308 // 2

    # Conquer
    min1_308, max1_308 = minmax308(
        A308[:mid308], count308
    )

    min2_308, max2_308 = minmax308(
        A308[mid308:], count308
    )

    # Combine: two comparisons
    count308[0] += 2

    if min1_308 < min2_308:
        minimum308 = min1_308
    else:
        minimum308 = min2_308

    if max1_308 > max2_308:
        maximum308 = max1_308
    else:
        maximum308 = max2_308

    return minimum308, maximum308


random.seed(308)

for n308 in [8, 64, 512, 4096]:

    A308 = [
        random.randint(1, 1000000)
        for _ in range(n308)
    ]

    count308 = [0]

    minimum308, maximum308 = minmax308(
        A308, count308
    )

    predicted308 = (3 * n308) // 2 - 2
    two_scan308 = 2 * n308 - 2

    print(
        n308,
        count308[0],
        predicted308,
        two_scan308
    )