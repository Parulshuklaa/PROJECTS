class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit=0
        minSoFar=prices[0]
        for p in prices[1:]:
            if p>minSoFar:
                profit+=(p-minSoFar)
            minSoFar=p
        return profit
# prices 
# max profit
# buy one and sell another, you can hold atmost one stock
# mutiple trasactions possible