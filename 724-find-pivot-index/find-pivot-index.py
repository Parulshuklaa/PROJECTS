class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        s,count=sum(nums),0
        for ind in range(len(nums)):
            count+=nums[ind]
            if count==s:
                return ind
            s-=nums[ind]
        return -1
    