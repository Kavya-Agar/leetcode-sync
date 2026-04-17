class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        # trick: xor
        number = 0
        for i in nums:
            number ^= i

        return number
