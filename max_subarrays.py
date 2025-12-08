# remove exactly one element from conflictingPairs, and hten count the number of non-empty subarrays of nums which do not contain both a and b for any remaining conflicting par [a, b]


def maxSubarrays(n, conflictingPairs):
    total = n * (n + 1) // 2  # Total number of subarrays

    def countInvalidSubarrays(pairs):
        """Count subarrays that contain both elements of at least one pair"""
        invalid = set()

        for a, b in pairs:
            if a > b:
                a, b = b, a
            # Subarrays containing both a and b:
            # Start from [1..a] and end at [b..n]
            for start in range(1, a + 1):
                for end in range(b, n + 1):
                    invalid.add((start, end))

        return len(invalid)

    maxValid = 0

    for idx in range(len(conflictingPairs)):
        remaining = conflictingPairs[:idx] + conflictingPairs[idx + 1 :]
        invalid = countInvalidSubarrays(remaining)
        valid = total - invalid
        maxValid = max(maxValid, valid)

    return maxValid


# Test with examples
print(maxSubarrays(4, [[2, 3], [1, 4]]))  # Expected: 9
print(maxSubarrays(5, [[1, 2], [2, 5], [3, 5]]))  # Expected: 12
