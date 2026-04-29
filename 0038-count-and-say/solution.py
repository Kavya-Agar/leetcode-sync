class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return "1"
            
        prev = self.countAndSay(n-1)
        return (self.RLE(prev))

    def RLE (self, prev):
        output = ""
        count = ""
        cur = ""
        for c in prev:
            if c != cur:
                output += str(count) + cur
                count = 1
                cur = c
            else:
                count +=1

        output += str(count) + cur
        return output

        
