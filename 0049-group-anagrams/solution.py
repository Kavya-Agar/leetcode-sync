class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        result = defaultdict(list)
        
        for s in strs:
            sortedString = ''.join(sorted(s))
            result[sortedString].append(s)
        
        return list(result.values())
