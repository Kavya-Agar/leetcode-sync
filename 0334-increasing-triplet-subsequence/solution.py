class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        minOne = float('inf')
        minTwo = float('inf')

        for num in nums:
            if num <= minOne:
                minOne = num
            elif num <= minTwo:
                minTwo = num
            else:
                return True
        
        return False
