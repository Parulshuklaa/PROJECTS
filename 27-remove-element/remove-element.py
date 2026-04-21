class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        nums.sort()
        a=0
        b=nums.count(val)
        for i in range(0,len(nums)):
            if nums[i]==val:
                a=i
                break
        while b>0:
            nums.pop(a)
            b-=1