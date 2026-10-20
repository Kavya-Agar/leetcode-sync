class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        if not nums:
            return 0

        currSum = maxSum = nums[0]
        
        for i in nums[1:]:
            currSum = max(i, currSum + i)
            maxSum = max(currSum, maxSum)
        
        return maxSum
