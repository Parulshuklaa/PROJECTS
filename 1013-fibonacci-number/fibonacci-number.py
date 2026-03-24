class Solution:
    def fib(self, n: int) -> int:
        if n <= 1:
            return n
        
        fib_ = [0] * (n + 1)
        fib_[1] = 1
        
        for i in range(2, n + 1):
            fib_[i] = fib_[i-1] + fib_[i-2]
        
        return fib_[n] 

        