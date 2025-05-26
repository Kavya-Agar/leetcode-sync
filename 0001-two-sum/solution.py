class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        mydict = {}

        for i in range(len(nums)):
            if target - nums[i] in mydict:
                return [mydict[target - nums[i]], i]

            mydict[nums[i]] = i
