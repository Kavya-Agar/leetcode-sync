class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)
        longest = 0

        for num in numSet:
            if num - 1 not in numSet:
                currNum = num
                currLong = 1
                
                while currNum + 1 in numSet:
                    currNum += 1
                    currLong += 1
                
                longest = max(longest, currLong)
        
        return longest
