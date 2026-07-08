class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = 'aeiou'
        count = sum(c in vowels for c in s[:k])
        maximum = count
        for i in range(len(s) - k):
            if s[i] in vowels:
                count -= 1
            if s[i+k] in vowels:
                count += 1
            maximum = max(maximum, count)
        
        return maximum
