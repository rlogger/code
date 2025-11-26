# need to eliminate duplicates

candidates = [5,2,6,7,1,10,1]
target = 8

def combinationSum(candidates, target):

    # sort the candidates first
    # 2 ^ n time complexity, worst case: n * 2^n
    # can't apply dp to this problem

    res = []

    candidates.sort()

    def dfs(i, cur, total):
        if total == target:
            res.append(cur.copy())
            return

        if total > target or i == len(candidates):
            return

        # include candidates[i]
        cur.append(candidates[i])
        dfs(i + 1, cur, total)
        cur.pop()

        # skip candidates[i[
        while i + 1 < len(candidates) and chandidates[i] == candidates[i + 1]:
            i += 1
        dfs(i + 1, cur, total)

    dfs(0, [], 0)

    return res

