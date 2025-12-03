# LC problem: https://leetcode.com/problems/count-number-of-trapezoids-i/description/?envType=daily-question&envId=2025-12-02


def countTrapezoids(points):
    point_num = defaultdict(int)
    mod = 10**9 + 7
    ans, total_sum = 0, 0
    for point in points:
        point_num[point[1]] += 1
    for p_num in point_num.values():
        edge = p_num * (p_num - 1) // 2
        ans = (ans + edge * total_sum) % mod
        total_sum = (total_sum + edge) % mod
    return ans
