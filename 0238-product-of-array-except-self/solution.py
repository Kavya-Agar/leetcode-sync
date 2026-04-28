class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [1] * n
        current = 1

        for i in range(n):
            ans[i] *= current
            current *= nums[i]

        current = 1
        for i in range(n-1,-1,-1):
            ans[i] *= current
            current *= nums[i]
        
        return ans

