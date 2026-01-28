from typing import List
from collections import defaultdict
from math import inf


class Solution:
    def minCost(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])

        # f[t][i][j] = min cost to reach (i,j) having used t teleports
        f = [[[inf] * n for _ in range(m)] for _ in range(k + 1)]

        # Base case: no teleports, just regular DP
        f[0][0][0] = 0
        for i in range(m):
            for j in range(n):
                if i > 0:
                    f[0][i][j] = min(f[0][i][j], f[0][i - 1][j] + grid[i][j])
                if j > 0:
                    f[0][i][j] = min(f[0][i][j], f[0][i][j - 1] + grid[i][j])

        # Group cells by value
        g = defaultdict(list)
        for i in range(m):
            for j in range(n):
                g[grid[i][j]].append((i, j))

        # Sort values in descending order
        keys = sorted(g.keys(), reverse=True)

        # Process each teleport round
        for t in range(1, k + 1):
            mn = inf
            # Process values in descending order
            # Cells with value v can teleport to any cell with value <= v
            # By processing high values first, we accumulate the minimum cost
            # that any lower-value cell can inherit
            for val in keys:
                positions = g[val]
                # Update running minimum from previous teleport round
                for i, j in positions:
                    mn = min(mn, f[t - 1][i][j])
                # All cells with this value can teleport here for free
                for i, j in positions:
                    f[t][i][j] = mn

            # Standard DP propagation (right/down moves)
            for i in range(m):
                for j in range(n):
                    if i > 0:
                        f[t][i][j] = min(f[t][i][j], f[t][i - 1][j] + grid[i][j])
                    if j > 0:
                        f[t][i][j] = min(f[t][i][j], f[t][i][j - 1] + grid[i][j])

        # Answer is minimum across all teleport counts
        return min(f[t][m - 1][n - 1] for t in range(k + 1))
