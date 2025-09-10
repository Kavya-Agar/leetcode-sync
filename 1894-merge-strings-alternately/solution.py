class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        newString = []
        if (len(word1) < len(word2)):
            for i in range(len(word1)):
                newString.append(word1[i])
                newString.append(word2[i])
            newString.append(word2[len(word1):])
        else:
            for i in range(len(word2)):
                newString.append(word1[i])
                newString.append(word2[i])
            newString.append(word1[len(word2):])
         
        return ''.join(newString)
