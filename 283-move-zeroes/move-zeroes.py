class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        pos = 0  # position for next non-zero element

        # Move non-zero elements forward
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[pos] = nums[i]
                pos += 1

        # Fill remaining positions with zero
        for i in range(pos, len(nums)):
            nums[i] = 0

        