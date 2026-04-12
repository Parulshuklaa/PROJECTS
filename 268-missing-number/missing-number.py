class Solution:
    def missingNumber(self, nums: List[int]) -> int:
       
        # count = 0 
        # for i in range(0,len(nums)+1):
        #     if i not in nums:
        #         count = i 
        # return count
         
        n = len(nums)
        tsum = n*(n+1)//2 
        asum= sum(nums)
        return tsum - asum 

