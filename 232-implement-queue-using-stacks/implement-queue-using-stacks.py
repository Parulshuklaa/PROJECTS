class MyQueue:

    def __init__(self):
        self.stack = []
        self.opstack = []

    def push(self, x: int) -> None:
        self.stack.append(x)

    def pop(self) -> int:
        if not self.opstack:
            while self.stack:
                self.opstack.append(self.stack.pop())
        return self.opstack.pop()

    def peek(self) -> int:
        if not self.opstack:
            while self.stack:
                self.opstack.append(self.stack.pop())
        return self.opstack[-1]

    def empty(self) -> bool:
        return len(self.stack) == 0 and len(self.opstack) == 0


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
        


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()