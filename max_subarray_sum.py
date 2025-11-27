from math import inf
from typing import List

def maxSubarraySum(nums, k):
    n = len(nums)
    min_prefix = {}

    min_prefix[0] = 0

    max_sum = float('-inf')
    prefix_sum = 0

    for i in range(n):
        prefix_sum += nums[i]
        remainder = (i + 1) % k

        if remainder in min_prefix:
            max_sum = max(max_sum, prefix_sum - min_prefix[remainder])

        if remainder not in min_predix:
            min_prefix[remainder] = prefix_sum
        else:
            min_prefix[remainder] = min(min_prefix[remainder], prefix_sum)

    return max_sum
