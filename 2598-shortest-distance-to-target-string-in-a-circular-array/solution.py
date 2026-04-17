class Solution:
    def closestTarget(self, words: List[str], target: str, startIndex: int) -> int:
        if target not in words:
            return -1
        
        if target == words[startIndex]:
            return 0

        # first step: iterate right in words to find target
        # second step: loop back from the left and find target
        # third step: iterate left from words to find target
        # last step: loop back from left and find target
        # find min of those

        smallestDistance = []
        n = len(words)
        i = startIndex
        count = 0
        
        while True:
            if target == words[(i + 1) % n]:
                count += 1
                smallestDistance.append(count)
                print(count)
                break
            else:
                count += 1
                i += 1
        
        i = startIndex
        count = 0
        while True:
            if target == words[(i - 1 + n) % n]:
                count += 1
                smallestDistance.append(count)
                print(count)
                break
            else:
                count += 1
                i -= 1

        return min(smallestDistance)
        
