class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
         from typing import List
         n = len(nums)
         answer = [1] * n

        # Step 1: left products
         left = 1
         for i in range(n):
            answer[i] = left
            left *= nums[i]

        # Step 2: right products
         right = 1
         for i in range(n - 1, -1, -1):
            answer[i] *= right
            right *= nums[i]

         return answer
