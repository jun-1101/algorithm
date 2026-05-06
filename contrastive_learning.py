"""
Assignment 1 – Contrastive Learning
====================================
只用 Python 標準庫：import math  （無任何套件）

D(x)：直接讀圖片原始位元組，等距取樣 N 個 byte，
      除以 255 後 L2 正規化 → N 維向量。
      兩張圖相減即得距離。

正樣本損失：L_pos = ||D(x1) - D(x2)||_2
負樣本損失：L_neg = max(0, C - ||D(x1) - D(x2)||_2)
"""

import math


N = 3000   # 取樣點數（每張圖取 N 個 byte）
C = 1.0    # margin


def to_vector(path):
    """
    圖片 → N 維向量（純標準庫）

    步驟：
      1. 以 binary 模式讀取圖片檔案的原始位元組
      2. 從中等距取樣 N 個位元組
      3. 除以 255 → 值域 [0, 1]
      4. L2 正規化 → 落在單位球面
    """
    with open(path, "rb") as f:
        raw = f.read()                              # 讀取所有位元組

    total = len(raw)
    # 等距取樣 N 個位置
    indices = [int(i * total / N) for i in range(N)]
    samples = [raw[i] / 255.0 for i in indices]    # byte值 → [0,1]

    # L2 正規化
    norm = math.sqrt(sum(x ** 2 for x in samples))
    return [x / (norm + 1e-8) for x in samples]


def l1(a, b):
    """L1 距離：||a - b||_1 = Σ|aᵢ - bᵢ|"""
    return sum(abs(a[i] - b[i]) for i in range(N))

def l2(a, b):
    """L2 距離：||a - b||_2 = √Σ(aᵢ - bᵢ)²"""
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(N)))


# ── 載入圖片 ──────────────────────────────────────────────
dog  = to_vector("1.jpeg")   # 狗
cat2 = to_vector("2.avif")    # 貓
cat1 = to_vector("3.webp")   # 貓

# ── 計算距離與損失 ────────────────────────────────────────
pairs = [
    ("cat1 (tabby)",  "cat2 (kitten)",   cat1, cat2, "POSITIVE"),
    ("dog (retriever)", "cat1 (tabby)",  dog,  cat1, "NEGATIVE"),
    ("dog (retriever)", "cat2 (kitten)", dog,  cat2, "NEGATIVE"),
]

print("=" * 62)
print("  Assignment 1 - Contrastive Learning")
print("  （圖片原始位元組直接相減，無任何套件）")
print("=" * 62)
print(f"  取樣維度 N = {N}，Margin C = {C}")
print()
print(f"  {'Pair':38s} {'L1':>8} {'L2':>8} {'Loss':>10}")
print("-" * 62)

pos_L  = None
neg_Ls = []

for name1, name2, v1, v2, ptype in pairs:
    d1 = l1(v1, v2)
    d2 = l2(v1, v2)

    if ptype == "POSITIVE":
        L     = d2                        # L = ||D(x1) - D(x2)||_2
        pos_L = L
    else:
        L = max(0.0, C - d2)              # L = max(0, C - ||D(x1) - D(x2)||_2)
        neg_Ls.append(L)

    pair_str = f"({name1} vs {name2})"
    if ptype == "POSITIVE":
        status = "↓ pull closer"
    else:
        status = "✓ ok" if d2 >= C else "✗ margin violated"

    print(f"  [{ptype[:3]}] {pair_str:34s} {d1:8.4f} {d2:8.4f} {L:>10.4f}  {status}")

L_total = pos_L + sum(neg_Ls)
print("-" * 62)
print(f"  L_pos = {pos_L:.4f}")
print(f"  ΣL_neg = {sum(neg_Ls):.4f}  "
      f"({' + '.join(f'{v:.4f}' for v in neg_Ls)})")
print(f"  L_total = {L_total:.4f}")
print("=" * 62)

# ── 相似度排名 ────────────────────────────────────────────
print()
print("=" * 62)
print("  相似度排名（L2 距離越小 = 越像）")
print("-" * 62)

all_pairs = [
    ("dog  (1.jpeg)", "cat1 (3.webp)", dog,  cat1),
    ("dog  (1.jpeg)", "cat2 (2.avif)",  dog,  cat2),
    ("cat1 (3.webp)", "cat2 (2.avif)",  cat1, cat2),
]

ranked = sorted(all_pairs, key=lambda x: l2(x[2], x[3]))

for rank, (n1, n2, v1, v2) in enumerate(ranked, 1):
    d = l2(v1, v2)
    bar = "█" * int(d * 40)
    print(f"  #{rank}  {n1}  vs  {n2}")
    print(f"       L2 = {d:.4f}  {bar}")

print()
print(f"  → 最像  ：{ranked[0][0]}  vs  {ranked[0][1]}")
print(f"  → 最不像：{ranked[-1][0]}  vs  {ranked[-1][1]}")
print("=" * 62)