class Solution:
    def partition(self, s: str) -> List[List[str]]:
        res = []
        def backtrack(start, path): 
            if start == len(s):
                res.append(path[:])
                return 

            for end in range(start, len(s)):
                part = s[start : end+1]
                
                if part == part[::-1]: 
                    path.append(part)

                    backtrack(end+1, path)

                    path.pop()

        backtrack(0, [])
        return res 



        