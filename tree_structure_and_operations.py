import collections

class TreeNode:
    """二元樹節點類別"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.children = [] # 用於一般有根樹

class BinaryTree:
    """二元樹類別"""
    def __init__(self, root_value=None):
        if root_value is not None:
            self.root = TreeNode(root_value)
        else:
            self.root = None

    def insert_left(self, parent_node, value):
        """在父節點左側插入新節點"""
        if parent_node.left is None:
            parent_node.left = TreeNode(value)
            parent_node.left.parent = parent_node
        else:
            new_node = TreeNode(value)
            new_node.left = parent_node.left
            parent_node.left.parent = new_node
            parent_node.left = new_node
            new_node.parent = parent_node
        return parent_node.left

    def insert_right(self, parent_node, value):
        """在父節點右側插入新節點"""
        if parent_node.right is None:
            parent_node.right = TreeNode(value)
            parent_node.right.parent = parent_node
        else:
            new_node = TreeNode(value)
            new_node.right = parent_node.right
            parent_node.right.parent = new_node
            parent_node.right = new_node
            new_node.parent = parent_node
        return parent_node.right

    def get_height(self, node=None, is_root_call=True):
        """計算樹的高度"""
        if is_root_call and node is None:
            node = self.root
        if node is None:
            return -1
        if not hasattr(node, 'left'): # 處理一般有根樹節點
            if not node.children:
                return 0
            return 1 + max(self.get_height(child, False) for child in node.children)
        
        # 處理二元樹節點
        if node.left is None and node.right is None:
            return 0
        left_h = self.get_height(node.left, False) if node.left else -1
        right_h = self.get_height(node.right, False) if node.right else -1
        return 1 + max(left_h, right_h)

    def count_nodes(self, node=None, is_root_call=True):
        """計算節點總數"""
        if is_root_call and node is None:
            node = self.root
        if node is None:
            return 0
        return 1 + self.count_nodes(node.left, False) + self.count_nodes(node.right, False)

    def is_balanced(self, node=None):
        """檢查樹是否平衡"""
        if node is None:
            node = self.root
        if node is None:
            return True
        
        def check_balance(curr):
            if curr is None:
                return True, -1
            left_bal, left_h = check_balance(curr.left)
            if not left_bal: return False, 0
            right_bal, right_h = check_balance(curr.right)
            if not right_bal: return False, 0
            
            balanced = abs(left_h - right_h) <= 1
            height = 1 + max(left_h, right_h)
            return balanced, height
            
        return check_balance(node)[0]

class TreeTraversal:
    """樹的走訪方法"""
    @staticmethod
    def preorder(node, result=None):
        if result is None: result = []
        if node:
            result.append(node.value)
            TreeTraversal.preorder(node.left, result)
            TreeTraversal.preorder(node.right, result)
        return result

    @staticmethod
    def inorder(node, result=None):
        if result is None: result = []
        if node:
            TreeTraversal.inorder(node.left, result)
            result.append(node.value)
            TreeTraversal.inorder(node.right, result)
        return result

    @staticmethod
    def postorder(node, result=None):
        if result is None: result = []
        if node:
            TreeTraversal.postorder(node.left, result)
            TreeTraversal.postorder(node.right, result)
            result.append(node.value)
        return result

    @staticmethod
    def level_order(node):
        if not node: return []
        result = []
        queue = collections.deque([node])
        while queue:
            curr = queue.popleft()
            result.append(curr.value)
            if curr.left: queue.append(curr.left)
            if curr.right: queue.append(curr.right)
        return result

class RootedTree:
    """一般有根樹類別"""
    def __init__(self, root_value):
        self.root = TreeNode(root_value)

    def add_child(self, parent_node, child_value):
        """添加子節點"""
        child_node = TreeNode(child_value)
        child_node.parent = parent_node
        parent_node.children.append(child_node)
        return child_node

    def get_height(self, node=None):
        """計算高度"""
        if node is None:
            node = self.root
        if not node.children:
            return 0
        return 1 + max(self.get_height(child) for child in node.children)

    def get_depth(self, node):
        """計算節點深度"""
        depth = 0
        curr = node
        while curr.parent:
            depth += 1
            curr = curr.parent
        return depth

    def is_ancestor(self, ancestor, descendant):
        """檢查是否為祖先"""
        curr = descendant
        while curr:
            if curr == ancestor:
                return True
            curr = curr.parent
        return False

# 示例用法
if __name__ == "__main__":
    print("=" * 50)
    print("二元樹示例")
    print("=" * 50)
    
    bt = BinaryTree(1)
    bt.insert_left(bt.root, 2)
    bt.insert_right(bt.root, 3)
    bt.insert_left(bt.root.left, 4)
    bt.insert_right(bt.root.left, 5)
    
    print("樹的結構：")
    print("       1")
    print("      / \\")
    print("     2   3")
    print("    / \\")
    print("   4   5")
    print()
    
    print(f"前序走訪： {TreeTraversal.preorder(bt.root)}")
    print(f"中序走訪： {TreeTraversal.inorder(bt.root)}")
    print(f"後序走訪： {TreeTraversal.postorder(bt.root)}")
    print(f"層序走訪： {TreeTraversal.level_order(bt.root)}")
    print()
    
    print(f"樹的高度： {bt.get_height()}")
    print(f"節點數量： {bt.count_nodes()}")
    print(f"是否平衡： {bt.is_balanced()}")

    print("\n" + "=" * 50)
    print("有根樹示例")
    print("=" * 50)
    
    rt = RootedTree("A")
    node_b = rt.add_child(rt.root, "B")
    node_c = rt.add_child(rt.root, "C")
    node_d = rt.add_child(node_b, "D")
    node_e = rt.add_child(node_b, "E")
    node_f = rt.add_child(node_c, "F")
    
    print("樹的結構：")
    print("       A")
    print("      / \\")
    print("     B   C")
    print("    / \\   \\")
    print("   D   E   F")
    print()
    
    print(f"樹的高度： {rt.get_height()}")
    print(f"D 的深度： {rt.get_depth(node_d)}")
    print(f"B 是 E 的祖先： {rt.is_ancestor(node_b, node_e)}")
    print(f"B 是 F 的祖先： {rt.is_ancestor(node_b, node_f)}")
