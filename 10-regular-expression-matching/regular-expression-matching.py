import re
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        a=re.findall(p,s)
        if len(a)>0:
            if a[0]==s:
                return True
            else:
                return False
        else:
            return False
        