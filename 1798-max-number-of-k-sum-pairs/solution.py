class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        nums.sort()
        count = 0
        i = 0
        j = len(nums) - 1

        while i < j:
            total = nums[i] + nums[j]

            if total == k:
                count += 1
                i += 1
                j -= 1
            elif total > k:
                j -= 1
            else:
                i += 1
        
        return count
