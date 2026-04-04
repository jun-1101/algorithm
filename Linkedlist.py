import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def search(self, key):
        """
        搜尋具有給定鍵值的節點。
        時間複雜度：O(n) - 在最壞情況下，我們需要遍歷整個串列。
        """
        start_time = time.perf_counter()
        current = self.head
        while current:
            if current.data == key:
                end_time = time.perf_counter()
                print(f"搜尋操作耗時: {end_time - start_time:.8f} 秒")
                return current
            current = current.next
        end_time = time.perf_counter()
        print(f"搜尋操作耗時: {end_time - start_time:.8f} 秒")
        return None

    def insert_at_beginning(self, data):
        """
        在串列開頭插入新節點。
        時間複雜度：O(1) - 常數時間，因為我們只需更新頭指標。
        """
        start_time = time.perf_counter()
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        end_time = time.perf_counter()
        print(f"在開頭插入操作耗時: {end_time - start_time:.8f} 秒")

    def insert_after(self, prev_node, data):
        """
        在已知節點後插入新節點。
        時間複雜度：O(1) - 常數時間，因為我們只需更新已知節點的指標。
        """
        start_time = time.perf_counter()
        if not prev_node:
            print("前一個節點必須存在於鏈結串列中。")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        end_time = time.perf_counter()
        print(f"在節點後插入操作耗時: {end_time - start_time:.8f} 秒")

    def delete_node(self, key):
        """
        刪除第一個出現的具有給定鍵值的節點。
        時間複雜度：O(n) - 在最壞情況下，我們需要遍歷以找到該節點及其前驅節點。
        """
        start_time = time.perf_counter()
        temp = self.head

        if temp is not None:
            if temp.data == key:
                self.head = temp.next
                temp = None
                end_time = time.perf_counter()
                print(f"刪除操作耗時: {end_time - start_time:.8f} 秒")
                return

        prev = None
        while temp is not None:
            if temp.data == key:
                break
            prev = temp
            temp = temp.next

        if temp == None:
            end_time = time.perf_counter()
            print(f"刪除操作耗時: {end_time - start_time:.8f} 秒")
            return

        prev.next = temp.next
        temp = None
        end_time = time.perf_counter()
        print(f"刪除操作耗時: {end_time - start_time:.8f} 秒")

    def display(self):
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) + " -> None")

if __name__ == "__main__":
    llist = LinkedList()
    
    print("--- 執行鏈結串列操作 ---")
    
    print("\n在開頭插入 10, 20, 30:")
    llist.insert_at_beginning(10)
    llist.insert_at_beginning(20)
    llist.insert_at_beginning(30)
    
    print("\n目前串列內容:")
    llist.display()

    print("\n搜尋 20:")
    result = llist.search(20)
    print("結果: " + ("已找到" if result else "未找到"))

    print("\n在 20 之後插入 25:")
    llist.insert_after(result, 25)
    llist.display()

    print("\n刪除 20:")
    llist.delete_node(20)
    llist.display()
    
    print("\n--- 操作結束 ---")    