import time
from collections import deque

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        print(f"Push: {item}")

    def pop(self):
        if not self.is_empty():
            item = self.items.pop()
            print(f"Pop: {item}")
            return item
        return None

    def is_empty(self):
        return len(self.items) == 0


class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)
        print(f"Enqueue: {item}")

    def dequeue(self):
        if not self.is_empty():
            item = self.items.popleft()
            print(f"Dequeue: {item}")
            return item
        return None

    def is_empty(self):
        return len(self.items) == 0


if __name__ == "__main__":

    print("=== Stack 過程 ===")
    stack = Stack()
    
    start_stack = time.time()

    for i in range(10):
        stack.push(i)

    for i in range(10):
        stack.pop()

    end_stack = time.time()
    print(f"Stack 總時間: {end_stack - start_stack:.6f} 秒\n")


    print("=== Queue 過程 ===")
    queue = Queue()
    
    start_queue = time.time()

    for i in range(10):
        queue.enqueue(i)

    for i in range(10):
        queue.dequeue()

    end_queue = time.time()
    print(f"Queue 總時間: {end_queue - start_queue:.6f} 秒")