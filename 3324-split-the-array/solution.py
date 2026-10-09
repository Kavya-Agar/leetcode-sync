class Solution:
    def isPossibleToSplit(self, nums: List[int]) -> bool:
        count = {}

        for i in nums:
            count[i] = 1 + count.get(i, 0)
        
        for val in count.values():
            if val > 2:
                return False
        
        return True
