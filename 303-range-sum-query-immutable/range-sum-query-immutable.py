class NumArray:
    def __init__(self, nums: List[int]):
        # Initialize the prefix_sum array with a 0 at the start
        self.prefix_sum = [0]
        
        # Precompute the prefix sums
        for num in nums:
            self.prefix_sum.append(self.prefix_sum[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        # Calculate the sum of elements from left to right using the prefix_sum array
        return self.prefix_sum[right + 1] - self.prefix_sum[left]