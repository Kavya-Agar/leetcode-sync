class MinStack:

    def __init__(self):
        self.stack = []          # main stack storing all values
        self.min_stack = []      # parallel stack tracking running minimum

    def push(self, value: int) -> None:
        self.stack.append(value)
        if not self.min_stack:
            self.min_stack.append(value)          # first element is always the min
        else:
            self.min_stack.append(min(self.min_stack[-1], value))  # preserve running min

    def pop(self) -> None:
        if not self.stack:
            return
        self.stack.pop()
        self.min_stack.pop()      # always pop both together to stay in sync

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]  # current min 
# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(value)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
