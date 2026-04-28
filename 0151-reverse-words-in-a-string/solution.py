class Solution:
    def reverseWords(self, s: str) -> str:
        emptyString = ""
        listOfWords = s.split()
        n = len(listOfWords)
        i = n - 1
        while i != -1:
            if i == 0:
                emptyString += listOfWords[i]
                break

            emptyString = emptyString + listOfWords[i] + " "
            i -= 1

        return emptyString
