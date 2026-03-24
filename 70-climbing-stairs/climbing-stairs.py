class Solution(object):
    def climbStairs(self, n):
        dp = {}
        
        def climb(n):
            if n in dp:
                return dp[n]
            if n <= 2:
                return n
            
            dp[n] = climb(n-1) + climb(n-2)
            return dp[n]
        
        return climb(n)
    
        
