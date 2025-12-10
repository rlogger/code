# LC #133: https://leetcode.com/problems/count-the-number-of-computer-unlocking-permutations


def count_permutations(complexity):
    n = len(complexity)
    for i in range(1, n):
        if complexity[i] <= complexity[0]:
            return 0

    ans, mod = 1, 10**9 + 7
    for i in range(2, n):
        ans = ans * i % mod

    return ans
