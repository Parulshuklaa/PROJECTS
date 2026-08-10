class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        out = []
        for i , j in zip(word1,word2):
            out.append(i)
            out.append(j)
        
        out.append(word1[len(word2):])
        out.append(word2[len(word1):])

        return "".join(out)
        
        