class Solution:
    def rob(self, nums: List[int]) -> int:
        dp = {}

        def solve(i):
            # base case
            if i >= len(nums):
                return 0

            # already computed
            if i in dp:
                return dp[i]

            # pick current house
            pick = nums[i] + solve(i + 2)

            # skip current house
            skip = solve(i + 1)

            # store result
            dp[i] = max(pick, skip)
            return dp[i]

        return solve(0)