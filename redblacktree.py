"""
演算法作業整合 - Assignments 1, 2, 3
========================================
  Assignment 1 : Red-Black Tree
  Assignment 2 : Hamming Distance
  Assignment 3 : Integral Image
========================================
"""

import time
import random


# ╔══════════════════════════════════════════════════════════════╗
#  ASSIGNMENT 1 — Red-Black Tree
# ╚══════════════════════════════════════════════════════════════╝

RED   = True
BLACK = False


class RBNode:
    def __init__(self, key):
        self.key    = key
        self.color  = RED
        self.left   = None
        self.right  = None
        self.parent = None

    def __repr__(self):
        c = "R" if self.color == RED else "B"
        return f"({self.key},{c})"


class RedBlackTree:
    def __init__(self):
        self.NIL       = RBNode(None)
        self.NIL.color = BLACK
        self.root      = self.NIL

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left   = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right  = x
        x.parent = y

    def insert(self, key):
        z        = RBNode(key)
        z.left   = self.NIL
        z.right  = self.NIL
        z.parent = None
        y, x     = None, self.root
        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            elif z.key > x.key:
                x = x.right
            else:
                return
        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left  = z
        else:
            y.right = z
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color        = BLACK
                    y.color               = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color        = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color        = BLACK
                    y.color               = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color        = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def search(self, key):
        node = self.root
        while node != self.NIL:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def delete(self, key):
        z = self.search(key)
        if z is None:
            return
        self._delete(z)

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left  = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def _delete(self, z):
        y                = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y                = self._minimum(z.right)
            y_original_color = y.color
            x                = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right        = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left        = z.left
            y.left.parent = y
            y.color       = z.color
        if y_original_color == BLACK:
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color        = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x       = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color      = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color        = x.parent.color
                    x.parent.color = BLACK
                    w.right.color  = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color        = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x       = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color       = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color        = x.parent.color
                    x.parent.color = BLACK
                    w.left.color   = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node != self.NIL:
            self._inorder(node.left, result)
            result.append(str(node))
            self._inorder(node.right, result)

    def print_tree(self, node=None, indent="", last=True):
        if node is None:
            node = self.root
        if node != self.NIL:
            prefix = "└── " if last else "├── "
            print(indent + prefix + str(node))
            indent += "    " if last else "│   "
            for i, child in enumerate([node.left, node.right]):
                self.print_tree(child, indent, i == 1)

    def black_height(self, node=None):
        if node is None:
            node = self.root
        if node == self.NIL:
            return 1
        lh = self.black_height(node.left)
        rh = self.black_height(node.right)
        if lh != rh:
            raise ValueError(f"黑高不一致！節點 {node}")
        return lh + (1 if node.color == BLACK else 0)


# ╔══════════════════════════════════════════════════════════════╗
#  ASSIGNMENT 2 — Hamming Distance
# ╚══════════════════════════════════════════════════════════════╝

class HammingDistance:

    @staticmethod
    def binary(s1: str, s2: str) -> int:
        if len(s1) != len(s2):
            raise ValueError(f"字串長度不同：{len(s1)} vs {len(s2)}")
        return sum(a != b for a, b in zip(s1, s2))

    @staticmethod
    def binary_xor(s1: str, s2: str) -> int:
        if len(s1) != len(s2):
            raise ValueError(f"字串長度不同：{len(s1)} vs {len(s2)}")
        return bin(int(s1, 2) ^ int(s2, 2)).count("1")

    @staticmethod
    def categorical(seq1: list, seq2: list) -> int:
        if len(seq1) != len(seq2):
            raise ValueError(f"序列長度不同：{len(seq1)} vs {len(seq2)}")
        return sum(a != b for a, b in zip(seq1, seq2))

    @staticmethod
    def integers(n1: int, n2: int) -> int:
        return bin(n1 ^ n2).count("1")

    @staticmethod
    def diff_positions(s1: str, s2: str) -> list:
        if len(s1) != len(s2):
            raise ValueError(f"字串長度不同：{len(s1)} vs {len(s2)}")
        return [i for i, (a, b) in enumerate(zip(s1, s2)) if a != b]

    @staticmethod
    def hamming_ball(center: str, candidates: list, radius: int) -> list:
        results = []
        for c in candidates:
            try:
                d = HammingDistance.binary(center, c)
                if d <= radius:
                    results.append((c, d))
            except ValueError:
                pass
        return sorted(results, key=lambda x: x[1])


# ╔══════════════════════════════════════════════════════════════╗
#  ASSIGNMENT 3 — Integral Image
# ╚══════════════════════════════════════════════════════════════╝

class IntegralImage:

    def __init__(self, image: list[list[int]]):
        if not image or not image[0]:
            raise ValueError("影像不可為空。")
        self.H     = len(image)
        self.W     = len(image[0])
        self.image = image
        self.II    = self._build(image)

    def _build(self, image: list[list[int]]) -> list[list[int]]:
        H, W = self.H, self.W
        II   = [[0] * (W + 1) for _ in range(H + 1)]
        for i in range(1, H + 1):
            row_sum = 0
            for j in range(1, W + 1):
                row_sum  += image[i - 1][j - 1]
                II[i][j]  = II[i - 1][j] + row_sum
        return II

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        if not (0 <= r1 <= r2 < self.H and 0 <= c1 <= c2 < self.W):
            raise IndexError(
                f"座標越界 (r1={r1},c1={c1},r2={r2},c2={c2})，"
                f"影像大小 {self.H}×{self.W}"
            )
        II = self.II
        return II[r2+1][c2+1] - II[r1][c2+1] - II[r2+1][c1] + II[r1][c1]

    def sliding_window_sums(self, kh: int, kw: int) -> list[list[int]]:
        return [
            [self.query(r, c, r+kh-1, c+kw-1)
             for c in range(self.W - kw + 1)]
            for r in range(self.H - kh + 1)
        ]

    def print_image(self):
        print("  Input Image:")
        for row in self.image:
            print("  ", " ".join(f"{v:3d}" for v in row))

    def print_integral(self):
        print("  Integral Image (with 0-padding):")
        for row in self.II:
            print("  ", " ".join(f"{v:4d}" for v in row))


# ╔══════════════════════════════════════════════════════════════╗
#  DEMO FUNCTIONS
# ╚══════════════════════════════════════════════════════════════╝

def section(title):
    print()
    print("═" * 60)
    print(f"  {title}")
    print("═" * 60)


def demo_rbt():
    section("ASSIGNMENT 1 — Red-Black Tree")
    rbt  = RedBlackTree()
    keys = [10, 20, 30, 15, 5, 25, 1, 7, 18]
    print(f"\n  插入順序：{keys}")
    for k in keys:
        rbt.insert(k)
    print("\n  【樹狀結構】")
    rbt.print_tree()
    print("  【中序遍歷】", rbt.inorder())
    print("  【黑高】    ", rbt.black_height())
    print(f"\n  search(15) → 找到 {rbt.search(15)}")
    print(f"  search(99) → 未找到")
    for k in [20, 10]:
        rbt.delete(k)
        print(f"  delete({k}) → 中序：{rbt.inorder()}")
    rbt2 = RedBlackTree()
    for i in range(10000):
        rbt2.insert(i)
    print(f"\n  插入 10000 筆後黑高：{rbt2.black_height()}")


def demo_hamming():
    section("ASSIGNMENT 2 — Hamming Distance")
    hd = HammingDistance()
    print("\n  【二進位字串】")
    for s1, s2 in [("1011101","1001001"),("0000000","1111111"),("1010101","1010101")]:
        print(f"  d({s1}, {s2}) = {hd.binary(s1, s2)}  差異位置：{hd.diff_positions(s1,s2)}")
    print("\n  【XOR 位元版本】")
    print(f"  d(1011101, 1001001) = {hd.binary_xor('1011101','1001001')}")
    print("\n  【整數 XOR】")
    for n1, n2 in [(2143896,2233796),(0,15),(7,7)]:
        print(f"  d({n1}, {n2}) = {hd.integers(n1, n2)}")
    print("\n  【類別序列】")
    seq1 = [2,1,4,3,8,9,6]; seq2 = [2,2,3,3,7,9,6]
    print(f"  d({seq1}, {seq2}) = {hd.categorical(seq1, seq2)}")
    print("\n  【詞彙距離】")
    for w1, w2 in [("toned","roses"),("karolin","kathrin")]:
        print(f"  d({w1}, {w2}) = {hd.categorical(list(w1), list(w2))}")
    print("\n  【漢明球 center='1010', radius=1】")
    candidates = ["0010","1110","1011","0000","1010","1001"]
    for s, d in hd.hamming_ball("1010", candidates, radius=1):
        print(f"  {s}  distance={d}")


def demo_integral():
    section("ASSIGNMENT 3 — Integral Image")
    image = [
        [1,2,2,4,1],[3,4,1,5,2],[2,3,3,2,4],[4,1,5,4,6],[6,3,2,1,3],
    ]
    ii = IntegralImage(image)
    print(); ii.print_image()
    print(); ii.print_integral()
    print("\n  【矩形查詢驗證】")
    for r1,c1,r2,c2,exp,label in [
        (0,0,0,0, 1,"單一像素"),(0,0,0,1, 3,"第一列前兩個"),
        (0,0,1,1,10,"左上2×2"),(0,0,4,4,74,"整張圖"),(1,1,3,3,28,"中間3×3"),
    ]:
        got = ii.query(r1,c1,r2,c2)
        print(f"  {label:<12} = {got}  {'✓' if got==exp else '✗'}")
    print("\n  【3×3 滑動視窗】")
    for row in ii.sliding_window_sums(3, 3):
        print("  ", row)


# ╔══════════════════════════════════════════════════════════════╗
#  MAIN
# ╚══════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    t0 = time.perf_counter()
    demo_rbt()
    t1 = time.perf_counter()

    demo_hamming()
    t2 = time.perf_counter()

    demo_integral()
    t3 = time.perf_counter()

    print()
    print("═" * 50)
    print("  花費時間總結")
    print("═" * 50)
    print(f"  Assignment 1 (Red-Black Tree)  : {t1-t0:.6f} 秒")
    print(f"  Assignment 2 (Hamming Distance): {t2-t1:.6f} 秒")
    print(f"  Assignment 3 (Integral Image)  : {t3-t2:.6f} 秒")
    print("═" * 50)