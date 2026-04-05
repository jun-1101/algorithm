import collections

class TreeNode:
    """二元樹節點類別"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class TreeTraversal:
    """樹的走訪方法實作"""
    
    # --- 前序走訪 (Preorder) ---
    @staticmethod
    def preorder_recursive(node, result=None):
        """遞迴實作前序走訪"""
        if result is None: result = []
        if node:
            result.append(node.value)
            TreeTraversal.preorder_recursive(node.left, result)
            TreeTraversal.preorder_recursive(node.right, result)
        return result

    @staticmethod
    def preorder_iterative(node):
        """迭代實作前序走訪"""
        if not node: return []
        result = []
        stack = [node]
        while stack:
            curr = stack.pop()
            result.append(curr.value)
            if curr.right: stack.append(curr.right)
            if curr.left: stack.append(curr.left)
        return result

    # --- 中序走訪 (Inorder) ---
    @staticmethod
    def inorder_recursive(node, result=None):
        """遞迴實作中序走訪"""
        if result is None: result = []
        if node:
            TreeTraversal.inorder_recursive(node.left, result)
            result.append(node.value)
            TreeTraversal.inorder_recursive(node.right, result)
        return result

    @staticmethod
    def inorder_iterative(node):
        """迭代實作中序走訪"""
        result = []
        stack = []
        curr = node
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append(curr.value)
            curr = curr.right
        return result

    # --- 後序走訪 (Postorder) ---
    @staticmethod
    def postorder_recursive(node, result=None):
        """遞迴實作後序走訪"""
        if result is None: result = []
        if node:
            TreeTraversal.postorder_recursive(node.left, result)
            TreeTraversal.postorder_recursive(node.right, result)
            result.append(node.value)
        return result

    @staticmethod
    def postorder_iterative_two_stacks(node):
        """使用兩個堆疊實作後序走訪"""
        if not node: return []
        result = []
        stack1 = [node]
        stack2 = []
        while stack1:
            curr = stack1.pop()
            stack2.append(curr)
            if curr.left: stack1.append(curr.left)
            if curr.right: stack1.append(curr.right)
        while stack2:
            result.append(stack2.pop().value)
        return result

    @staticmethod
    def postorder_iterative_one_stack(node):
        """使用單個堆疊實作後序走訪"""
        if not node: return []
        result = []
        stack = []
        curr = node
        last_visited = None
        while stack or curr:
            if curr:
                stack.append(curr)
                curr = curr.left
            else:
                peek_node = stack[-1]
                if peek_node.right and last_visited != peek_node.right:
                    curr = peek_node.right
                else:
                    result.append(peek_node.value)
                    last_visited = stack.pop()
        return result

    # --- 層序走訪 (Level-order) ---
    @staticmethod
    def level_order(node):
        """層序走訪 (BFS)"""
        if not node: return []
        result = []
        queue = collections.deque([node])
        while queue:
            curr = queue.popleft()
            result.append(curr.value)
            if curr.left: queue.append(curr.left)
            if curr.right: queue.append(curr.right)
        return result

    @staticmethod
    def level_order_grouped(node):
        """按層級分組的層序走訪"""
        if not node: return []
        result = []
        queue = collections.deque([node])
        while queue:
            level_size = len(queue)
            level_nodes = []
            for _ in range(level_size):
                curr = queue.popleft()
                level_nodes.append(curr.value)
                if curr.left: queue.append(curr.left)
                if curr.right: queue.append(curr.right)
            result.append(level_nodes)
        return result

# 示例用法
if __name__ == "__main__":
    print("=" * 60)
    print("樹走訪示例")
    print("=" * 60)
    
    # 建立測試樹
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    print("樹的結構：")
    print("       1")
    print("      / \\")
    print("     2   3")
    print("    / \\")
    print("   4   5")
    print()
    
    print("前序走訪 (Preorder):")
    print(f"  遞迴: {TreeTraversal.preorder_recursive(root)}")
    print(f"  迭代: {TreeTraversal.preorder_iterative(root)}")
    
    print("\n中序走訪 (Inorder):")
    print(f"  遞迴: {TreeTraversal.inorder_recursive(root)}")
    print(f"  迭代: {TreeTraversal.inorder_iterative(root)}")
    
    print("\n後序走訪 (Postorder):")
    print(f"  遞迴: {TreeTraversal.postorder_recursive(root)}")
    print(f"  迭代 (2個棧): {TreeTraversal.postorder_iterative_two_stacks(root)}")
    print(f"  迭代 (1個棧): {TreeTraversal.postorder_iterative_one_stack(root)}")
    
    print("\n層序走訪 (Level-order):")
    print(f"  結果: {TreeTraversal.level_order(root)}")
    print(f"  按層: {TreeTraversal.level_order_grouped(root)}")

    # 複雜樹測試
    print("\n" + "=" * 60)
    print("複雜樹示例")
    print("=" * 60)
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(3)
    root2.left.left = TreeNode(4)
    root2.left.right = TreeNode(5)
    root2.right.right = TreeNode(6)
    root2.left.left.left = TreeNode(7)
    
    print("樹的結構：")
    print("         1")
    print("        / \\")
    print("       2   3")
    print("      / \\   \\")
    print("     4   5   6")
    print("    /")
    print("   7")
    print()
    print(f"前序: {TreeTraversal.preorder_recursive(root2)}")
    print(f"中序: {TreeTraversal.inorder_recursive(root2)}")
    print(f"後序: {TreeTraversal.postorder_recursive(root2)}")
    print(f"層序: {TreeTraversal.level_order(root2)}")
    print(f"按層: {TreeTraversal.level_order_grouped(root2)}")
