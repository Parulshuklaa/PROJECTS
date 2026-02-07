class Solution:
    def sortColors(self, nums: List[int]) -> None:
        n= len(nums)
        for i in range(n-1):
            for j in range(0, n - i-1):
                  if nums[j] > nums[j + 1]:
                     nums[j], nums[j+1] = nums[j+1], nums[j] 


#for v in nums:
  #if v==0:
    #count0+=1
  #elif v==1:
    #count1+=1
  #else:
    #count2+=1
#count0=count1=count2=0
#ind>0
#while (ind < count2):
    #nums[ind]=1
    #ind +=1 
