class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        summ = nums[0]
        maxsum = nums[0]

        for i in range(1, len(nums)):
            summ = max(nums[i], summ + nums[i])  # extend or restart
            maxsum = max(summ, maxsum)

        return maxsum
 