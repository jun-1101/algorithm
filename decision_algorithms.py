from collections import deque
import math
import time


# ============================================================
# 1. BFS - 廣度優先搜尋（人際網路）
#    時間複雜度：O(V + E)，V = 節點數，E = 邊數
# ============================================================

def bfs_shortest_path(graph: dict, start: str, end: str) -> tuple[list, int]:
    if start == end:
        return [start], 0

    visited = {start: None}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited[neighbor] = current
                if neighbor == end:
                    path = []
                    node = end
                    while node is not None:
                        path.append(node)
                        node = visited[node]
                    path.reverse()
                    return path, len(path) - 1
                queue.append(neighbor)

    return [], -1


# ============================================================
# 2. Dijkstra - 加權圖形最短路徑
#    時間複雜度：O(V²)，僅適用於非負權重
# ============================================================

def dijkstra(graph: dict, start: str) -> tuple[dict, dict]:
    nodes = list(graph.keys())
    for neighbors in graph.values():
        for neighbor, _ in neighbors:
            if neighbor not in nodes:
                nodes.append(neighbor)

    distance = {node: math.inf for node in nodes}
    done = {node: False for node in nodes}
    previous = {node: None for node in nodes}
    distance[start] = 0

    for _ in range(len(nodes)):
        current = None
        for node in nodes:
            if not done[node]:
                if current is None or distance[node] < distance[current]:
                    current = node

        if current is None or distance[current] == math.inf:
            break

        done[current] = True

        for neighbor, weight in graph.get(current, []):
            new_dist = distance[current] + weight
            if new_dist < distance[neighbor]:
                distance[neighbor] = new_dist
                previous[neighbor] = current

    return distance, previous


def reconstruct_path(previous: dict, start: str, end: str) -> list:
    """根據 previous 字典回溯最短路徑。"""
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    if path[0] == start:
        return path
    return []


# ============================================================
# 3. Bellman-Ford - 含負權重的最短路徑
#    時間複雜度：O(V × E)
# ============================================================

def bellman_ford(edges: list, nodes: list, start: str) -> tuple[dict, dict, bool]:
    distance = {node: math.inf for node in nodes}
    previous = {node: None for node in nodes}
    distance[start] = 0

    for iteration in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if distance[u] != math.inf and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                previous[v] = u
                updated = True

        if not updated:
            print(f"  [提早結束] 第 {iteration + 1} 輪無更新，提早終止。")
            return distance, previous, False

    for u, v, w in edges:
        if distance[u] != math.inf and distance[u] + w < distance[v]:
            return distance, previous, True

    return distance, previous, False


# ============================================================
# 4. 0/1 背包問題 - 動態規劃 (DP)
#    時間複雜度：O(N × W)
# ============================================================

def knapsack_01(items: list[tuple], capacity: int) -> tuple[int, list, list[list]]:
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, w, v = items[i - 1]
        for j in range(capacity + 1):
            not_take = dp[i - 1][j]
            take = dp[i - 1][j - w] + v if j >= w else -1
            dp[i][j] = max(not_take, take)

    selected = []
    j = capacity
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selected.append(items[i - 1][0])
            j -= items[i - 1][1]
    selected.reverse()

    return dp[n][capacity], selected, dp


# ============================================================
# 主程式：示範與測試
# ============================================================

def print_section(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_bfs() -> float:
    print_section("1. BFS 廣度優先搜尋 — 人際網路")
    social_graph = {
        "Marshall": ["Sunny", "Amy", "John", "Uriah", "Yummy"],
        "Sunny":    ["Marshall", "Amy"],
        "Amy":      ["Marshall", "Sunny", "Cara"],
        "Cara":     ["Amy"],
        "John":     ["Marshall", "Bella", "Eric", "Andy"],
        "Bella":    ["John", "Eric"],
        "Eric":     ["John", "Bella"],
        "Uriah":    ["Marshall", "Andy"],
        "Andy":     ["John", "Uriah", "May"],
        "May":      ["Andy"],
        "Yummy":    ["Marshall"],
    }

    pairs = [("Marshall", "May"), ("Sunny", "May"), ("Cara", "Bella")]
    t_start = time.perf_counter()
    for start, end in pairs:
        path, dist = bfs_shortest_path(social_graph, start, end)
        if dist >= 0:
            print(f"  {start} → {end}：路徑 {' → '.join(path)}，距離 {dist} 步")
        else:
            print(f"  {start} → {end}：不可達")
    t_end = time.perf_counter()
    elapsed = t_end - t_start
    print(f"\n  執行時間：{elapsed:.6f} 秒 ({elapsed * 1000:.4f} ms)")
    return elapsed


def demo_dijkstra() -> float:
    print_section("2. Dijkstra — 加權圖形")
    graph = {
        "1": [("2", 4), ("3", 9), ("5", 5)],
        "2": [("1", 4), ("3", 2), ("4", 7), ("5", 4)],
        "3": [("1", 9), ("2", 2), ("4", 10)],
        "4": [("2", 7), ("3", 10), ("5", 4), ("6", 8)],
        "5": [("1", 5), ("2", 4), ("4", 4), ("6", 6)],
        "6": [("4", 8), ("5", 6)],
    }

    t_start = time.perf_counter()
    distance, previous = dijkstra(graph, "1")
    t_end = time.perf_counter()
    elapsed = t_end - t_start

    print(f"  起點：節點 1")
    print(f"  {'節點':<6} {'最短距離':<10} {'最短路徑'}")
    print(f"  {'-'*40}")
    for node in sorted(distance.keys()):
        d = distance[node]
        path = reconstruct_path(previous, "1", node)
        d_str = str(d) if d != math.inf else "∞"
        print(f"  {node:<6} {d_str:<10} {' → '.join(path)}")

    expected = {"1": 0, "2": 4, "3": 6, "4": 9, "5": 5, "6": 11}
    all_correct = all(distance[k] == v for k, v in expected.items())
    print(f"  執行時間：{elapsed:.6f} 秒 ({elapsed * 1000:.4f} ms)")
    return elapsed


def demo_bellman_ford() -> float:
    print_section("3. Bellman-Ford — 含負權重")
    nodes_neg = ["A", "B", "C"]
    edges_neg = [
        ("A", "B",   5),
        ("A", "C",  10),
        ("C", "B", -50),
    ]

    print("  圖形：A→B(5), A→C(10), C→B(-50)")
    print("  [說明] Dijkstra 無法處理此圖，因為有負權重邊 C→B(-50)")

    t_start = time.perf_counter()
    dist, prev, neg_cycle = bellman_ford(edges_neg, nodes_neg, "A")
    t_end = time.perf_counter()
    elapsed = t_end - t_start

    print(f"  Bellman-Ford 結果：")
    for node in nodes_neg:
        d = dist[node] if dist[node] != math.inf else "∞"
        path = reconstruct_path(prev, "A", node)
        print(f"    A → {node}：距離 {d}，路徑 {' → '.join(path) if path else '無'}")
    print(f"  存在負環：{neg_cycle}")
    print(f"  ✓ A→B 最短為 -40（經由 C），而非直接走 5")

    print("\n  [負環偵測示範]")
    nodes_cycle = ["X", "Y", "Z"]
    edges_cycle = [
        ("X", "Y",  1),
        ("Y", "Z", -3),
        ("Z", "X",  1),
    ]
    _, _, has_cycle = bellman_ford(edges_cycle, nodes_cycle, "X")
    print(f"  圖形 X→Y(1), Y→Z(-3), Z→X(1)，偵測到負環：{has_cycle}")

    print(f"\n  執行時間：{elapsed:.6f} 秒 ({elapsed * 1000:.4f} ms)")
    return elapsed


def demo_knapsack() -> float:
    print_section("4. 0/1 背包問題 — 動態規劃 DP")
    items = [
        ("物品A", 2, 3),
        ("物品B", 3, 4),
        ("物品C", 4, 5),
        ("物品D", 5, 8),
        ("物品E", 9, 10),
    ]
    capacity = 10

    print(f"  背包容量：{capacity}")
    print(f"  {'物品':<8} {'重量W':<8} {'價值V':<8}")
    print(f"  {'-'*24}")
    for name, w, v in items:
        print(f"  {name:<8} {w:<8} {v:<8}")

    t_start = time.perf_counter()
    max_val, selected, dp = knapsack_01(items, capacity)
    t_end = time.perf_counter()
    elapsed = t_end - t_start

    print(f"\n  DP 表格 dp[物品][容量]：")
    header = "        " + " ".join(f"{j:3}" for j in range(capacity + 1))
    print(f"  {header}")
    print(f"  {'容量→':8}" + "---" * (capacity + 1))
    for i, row in enumerate(dp):
        label = f"item{i}" if i > 0 else " 基準"
        print(f"  {label:<8}" + " ".join(f"{v:3}" for v in row))

    print(f"\n  最大價值：{max_val}")
    print(f"  選擇物品：{selected}")
    total_w = sum(w for name, w, v in items if name in selected)
    total_v = sum(v for name, w, v in items if name in selected)
    print(f"  總重量：{total_w}（≤ 容量 {capacity}）✓")
    print(f"  總價值：{total_v}")
    print(f"\n  執行時間：{elapsed:.6f} 秒 ({elapsed * 1000:.4f} ms)")
    return elapsed


if __name__ == "__main__":
    print("=" * 60)
    print("  最佳化決策演算法 — Lecture 9 作業")
    print("  從最短路徑到動態規劃的思維演進")
    print("=" * 60)

    total_start = time.perf_counter()

    t1 = demo_bfs()
    t2 = demo_dijkstra()
    t3 = demo_bellman_ford()
    t4 = demo_knapsack()

    total_end = time.perf_counter()
    total = total_end - total_start

    print("\n" + "=" * 60)
    print("  演算法複雜度與執行時間總結")
    print("=" * 60)
    print(f"  {'演算法':<20} {'時間複雜度':<12} {'執行時間':>16}  {'負權重'}")
    print(f"  {'-'*65}")
    print(f"  {'BFS':<20} {'O(V + E)':<12} {t1*1000:>12.4f} ms  不適用（無權重）")
    print(f"  {'Dijkstra':<20} {'O(V²)':<12} {t2*1000:>12.4f} ms  不允許")
    print(f"  {'Bellman-Ford':<20} {'O(V × E)':<12} {t3*1000:>12.4f} ms  完全允許")
    print(f"  {'Knapsack DP':<20} {'O(N × W)':<12} {t4*1000:>12.4f} ms  N/A（資源分配）")
    print(f"  {'-'*65}")
    print(f"  {'總計':<20} {'':<12} {total*1000:>12.4f} ms")