class Solution:
    def differenceOfSum(self, nums: List[int]) -> int:
        elsum = sum(nums)
        rem=0
        digitsum = []
        for i in nums:
            if i>=10:
                while (i>0):
                    rem=i%10
                    digitsum.append(rem)
                    i = i//10
            else:
                digitsum.append(i)
        d=sum(digitsum)
        return abs(d-elsum)
            


