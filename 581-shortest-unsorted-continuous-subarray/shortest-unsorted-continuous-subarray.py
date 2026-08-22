class Solution:
    def findUnsortedSubarray(self, nums):
        nums_sorted = sorted(nums)

        left = 0 
        right = len(nums) - 1

        while left < len(nums) and nums[left] == nums_sorted[left]:
            left += 1

        while right >= 0 and nums[right] == nums_sorted[right]:
            right -= 1

        if left > right:
            return 0

        return right - left + 1