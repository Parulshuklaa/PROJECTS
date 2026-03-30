class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        result = []
        temp = []
        def helpFunction(start, end, k):
            if k <=0:
                result.append(temp[:])
                return
            if start > end:
                return 
            temp.append(start)
            helpFunction(start +1 , end, k-1)
            temp.pop()
            helpFunction(start+1, end, k )

        helpFunction(1,n,k)
        return result 