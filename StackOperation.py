class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        print(f"Pushed: {item}")

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            print("Stack is empty")
            return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            print("Stack is empty")
            return None

    def is_empty(self):
        return len(self.items) == 0

    def display(self):
        print("Stack:", self.items)


if __name__ == "__main__":
    s = Stack()
    
    s.push(10)
    s.push(20)
    s.push(30)
    
    s.display()
    
    print("Top element:", s.peek())
    
    print("Popped:", s.pop())
    s.display()
    
    print("Is empty:", s.is_empty())