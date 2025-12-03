# LC: https://leetcode.com/problems/count-number-of-trapezoids-ii/description/?envType=daily-question&envId=2025-12-03


def countTrapezoids(points):
    # constraints: two of the lines have to stay parallel
    #   calculate the slope, store matching 2 inside a set
    #   another loop (same complexity), validate the last two points (makes a quadlateral)
    #       Final answer = total valid base-pairs minus parallelogram overcounts.

    n = len(points)
    inf = 10**9 + 7
    slope_to_intercept = defaultdict(int)
    mid_to_slope = defaultdict(list)
    ans = 0

    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dx = x1 - x2
            dy = y1 - y2

            if x2 == x1:
                k = inf
                b = x1
            else:
                k = (y2 - y1) / (x2 - x1)
                b = (y1 * dx - x1 * dy) / dx

            mid = (x1 + x2) * 10000 + (y1 + y2)
            slope_to_intercept[k].append(b)
            mid_to_slope[mid].append(k)

    for sti in slope_to_intercept.values():
        if len(sti) == 1:
            continue

        cnt = defaultdict(int)
        for b_val in sti:
            cnt[b_val] += 1

        total_sum = 0
        for count in cnt.values():
            ans += total_sum * count
            total_sum += count

    for mts in mid_to_slope.values():
        if len(mts) == 1:
            continue

        cnt = defaultdict(int)
        for k_val in mts:
            cnt[k_val] += 1

        total_sum = 0
        for count in cnt.values():
            ans -= total_sum * count
            total_sum += count

    return ans
