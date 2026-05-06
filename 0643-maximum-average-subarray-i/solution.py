class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        windowSum = sum(nums[:k])
        maxSum = windowSum

        for i in range(k, len(nums)):
            windowSum = windowSum - nums[i - k] + nums[i]
            if windowSum > maxSum:
                maxSum = windowSum

        return maxSum / k
