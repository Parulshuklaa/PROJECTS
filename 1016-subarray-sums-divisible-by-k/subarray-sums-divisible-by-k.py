class Solution:
    def subarraysDivByK(self, nums: list[int], k: int) -> int:
        map = {0: 1}
        prefix_sum = 0
        count = 0
        for num in nums:
            prefix_sum += num
            rem = prefix_sum % k
            if rem in map:
                count += map[rem]
                map[rem] += 1
            else:
                map[rem] = 1
           
        return count
