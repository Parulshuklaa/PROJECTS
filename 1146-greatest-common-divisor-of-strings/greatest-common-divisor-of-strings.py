import math

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # If concatenations differ, no common base string exists
        if str1 + str2 != str2 + str1:
            return ""

        len1 = len(str1)
        len2 = len(str2)

        # GCD of string lengths
        g = math.gcd(len1, len2)

        # GCD string is prefix of length g
        return str1[:g]