class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        count = 0 
        maxCount = 0 
        for i in nums:
            if i ==1:
                count+=1 
            else : 
                maxCount = max(count, maxCount)
                count = 0 
        return max(maxCount, count)
        