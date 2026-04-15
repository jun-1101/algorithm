import math
from collections import deque

# ============================================================
# Question 1. Sorting
# ============================================================

def bubble_sort(arr):
    n = len(arr)
    arr = arr[:]  # avoid modifying the original list
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

arr = [5, 1, 4, 2, 8]
print("Question 1. Sorting")
print(bubble_sort(arr))
print()
# Output: [1, 2, 4, 5, 8]

# ============================================================
# Question 2. Recurrence / Recursive Thinking
# ============================================================

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print("Question 2. Recurrence / Recursive Thinking")
print(factorial(5))
print()
# Output: 120

# ============================================================
# Question 3. Greedy and Dynamic Programming
# ============================================================

def min_coins(amount):
    coins = [25, 10, 5, 1]
    used = []
    for coin in coins:
        while amount >= coin:
            amount -= coin
            used.append(coin)
    return used

used = min_coins(63)
print("Question 3. Greedy and Dynamic Programming")
print("Number of coins:", len(used))
print("Coins used:", used)
print()
# Output:
# Number of coins: 6
# Coins used: [25, 25, 10, 1, 1, 1]

# ============================================================
# Question 4. Tree Construction and Search
# ============================================================

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def dfs_search(root, target):
    if root is None:
        return False
    if root.val == target:
        return True
    return dfs_search(root.left, target) or dfs_search(root.right, target)

root = Node(5,
            Node(3, Node(2), Node(4)),
            Node(8, None, Node(7)))

print("Question 4. Tree Construction and Search")
print("Found" if dfs_search(root, 7) else "Not Found")
print()
# Output: Found

# ============================================================
# Question 5. Stack and Queue
# ============================================================

# Stack
print("Question 5. Stack and Queue")
stack = []
stack.append(10)
stack.append(20)
stack.pop()
stack.append(30)
print("Stack:", stack)

# Queue
queue = deque()
queue.append(10)
queue.append(20)
queue.popleft()
queue.append(30)
print("Queue:", list(queue))
print()

# Output:
# Stack: [10, 30]
# Queue: [20, 30]

# ============================================================
# Question 6. Linked List
# ============================================================

class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)

curr = head
print("Question 6. Linked List")
while curr:
    print(curr.val, end=" ")
    curr = curr.next
print()
print()
# Output: 1 2 3 4

# ============================================================
# Question 7. Nearest Neighbor Classifier with L1 and L2 Distance
# ============================================================

A = (1, 1)
B = (4, 4)
C = (6, 1)
P = (3, 2)

def l1(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

def l2(p, q):
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

print("Question 7. Nearest Neighbor Classifier with L1 and L2 Distance")
print("L1 distances:")
print("A:", l1(P, A))
print("B:", l1(P, B))
print("C:", l1(P, C))

print("L2 distances:")
print("A:", round(l2(P, A), 3))
print("B:", round(l2(P, B), 3))
print("C:", round(l2(P, C), 3))

# Nearest neighbor:
# L1: A (distance 3), B (distance 3), C (distance 4)
# If a tie-break rule chooses the first encountered minimum, A is selected.
# L2: A (2.236), B (2.236), C (3.162)
# With the same tie-break rule, A is selected.
print("Nearest under both L1 and L2: A")