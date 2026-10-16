class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)
        countDict = dict(counts)
        sorted_dict = dict(sorted(countDict.items(), key=lambda item: item[1], reverse=True))
        return list(sorted_dict.keys())[:k]
