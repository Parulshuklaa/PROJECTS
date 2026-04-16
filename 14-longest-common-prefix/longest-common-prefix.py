class Solution:
    def longestCommonPrefix(self, strs):
        strs.sort()
        first = strs[0]
        last = strs[-1]
        
        i = 0
        while i < len(first) and first[i] == last[i]:
            i += 1
        
        return first[:i]