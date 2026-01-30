'''
You are given two 0-indexed strings source and target, both of length n and consisting of lowercase English characters. You are also given two 0-indexed string arrays original and changed, and an integer array cost, where cost[i] represents the cost of converting the string original[i] to the string changed[i].

You start with the string source. In one operation, you can pick a substring x from the string, and change it to y at a cost of z if there exists any index j such that cost[j] == z, original[j] == x, and changed[j] == y. You are allowed to do any number of operations, but any pair of operations must satisfy either of these two conditions:

The substrings picked in the operations are source[a..b] and source[c..d] with either b < c or d < a. In other words, the indices picked in both operations are disjoint.
The substrings picked in the operations are source[a..b] and source[c..d] with a == c and b == d. In other words, the indices picked in both operations are identical.
Return the minimum cost to convert the string source to the string target using any number of operations. If it is impossible to convert source to target, return -1.

Note that there may exist indices i, j such that original[j] == original[i] and changed[j] == changed[i].
'''

class TrieNode:
    def __init__(self):
        self.children = {}
        self.str_id = -1  # ID of string ending at this node (-1 if none)


class Solution:
    def minimumCost(self, source: str, target: str, original: list[str], changed: list[str], cost: list[int]) -> int:
        # Step 1: Build trie and assign IDs to unique strings
        root = TrieNode()
        str_to_id = {}

        def get_or_create_id(s: str) -> int:
            if s in str_to_id:
                return str_to_id[s]

            # Insert into trie
            node = root
            for c in s:
                if c not in node.children:
                    node.children[c] = TrieNode()
                node = node.children[c]

            # Assign new ID
            new_id = len(str_to_id)
            str_to_id[s] = new_id
            node.str_id = new_id
            return new_id

        # Register all strings and get their IDs
        for orig, chg in zip(original, changed):
            get_or_create_id(orig)
            get_or_create_id(chg)

        num_strings = len(str_to_id)

        # Step 2: Floyd-Warshall to find min cost between any two strings
        INF = float('inf')
        dist = [[INF] * num_strings for _ in range(num_strings)]

        # Self-conversion costs 0
        for i in range(num_strings):
            dist[i][i] = 0

        # Direct conversion costs
        for orig, chg, c in zip(original, changed, cost):
            orig_id = str_to_id[orig]
            chg_id = str_to_id[chg]
            dist[orig_id][chg_id] = min(dist[orig_id][chg_id], c)

        # Floyd-Warshall
        for k in range(num_strings):
            for i in range(num_strings):
                if dist[i][k] == INF:
                    continue
                for j in range(num_strings):
                    if dist[k][j] == INF:
                        continue
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        # Step 3: DP to find minimum cost to convert source to target
        n = len(source)
        dp = [INF] * (n + 1)
        dp[0] = 0

        for i in range(n):
            if dp[i] == INF:
                continue

            # Option 1: If characters match, skip (no conversion needed)
            if source[i] == target[i]:
                dp[i + 1] = min(dp[i + 1], dp[i])

            # Option 2: Find substrings starting at i that can be converted
            # Traverse trie simultaneously for source and target
            src_node = root
            tgt_node = root

            for j in range(i, n):
                src_char = source[j]
                tgt_char = target[j]

                # Both substrings must exist in trie
                if src_char not in src_node.children or tgt_char not in tgt_node.children:
                    break

                src_node = src_node.children[src_char]
                tgt_node = tgt_node.children[tgt_char]

                # If both substrings are registered strings, try conversion
                if src_node.str_id != -1 and tgt_node.str_id != -1:
                    conversion_cost = dist[src_node.str_id][tgt_node.str_id]
                    if conversion_cost != INF:
                        dp[j + 1] = min(dp[j + 1], dp[i] + conversion_cost)

        return dp[n] if dp[n] != INF else -1

