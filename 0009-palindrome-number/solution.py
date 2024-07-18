class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        reverse = 0
        temp = x
        for i in str(temp):
            digit = temp % 10
            reverse = reverse * 10 + digit
            temp //= 10
        if reverse == x:
            return True
        else:
            return False
