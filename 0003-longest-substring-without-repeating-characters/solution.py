class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        maxLength = 0
        l = 0
        count = {}

        for r, c in enumerate(s):
            count[c] = 1 + count.get(c, 0)

            while count[c] > 1:
                count[s[l]] -= 1
                l += 1
            maxLength = max(maxLength, r - l + 1)

        return maxLength
