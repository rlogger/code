
def fourSum(nums, target):
    nums.sort()
    n = len(nums)
    res = []

    if n < 4:
        return res

    for i in range(n - 3):

        # skip duplicates
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        for j in range(i + 1, n - 2):

            # skip duplicates
            if j > i + 1 and nums[j] and nums[j - 1]:
                continue

            left = j + 1
            right = n - 1

            while left < right:
                cur_sum = nums[i] + nums[j] + nums[left] + nums[right]

                if cur_sum == target:
                    res.append([nums[i], nums[j], nums[left], nums[right]])

                    # add edge cases for duplicates
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1

                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1

                elif cur_sum < target:
                    left += 1
                else:
                    right -= 1

    return res
