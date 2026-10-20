class Solution:
    def reverseWords(self, s: str) -> str:
        listOfWords = s.split()
        return " ".join(listOfWords[::-1])
