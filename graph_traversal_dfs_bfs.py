import collections

class Graph:
    """使用鄰接表表示的無向圖"""
    def __init__(self, num_vertices=0):
        self.num_vertices = num_vertices
        self.adj_list = collections.defaultdict(list)
        for i in range(num_vertices):
            self.adj_list[i] = []

    def add_edge(self, u, v, weight=1):
        """添加無向邊"""
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))

    def get_vertices(self):
        """獲取所有頂點"""
        return list(self.adj_list.keys())

    def display(self):
        """顯示圖的結構"""
        print("圖（鄰接表）：")
        for vertex in sorted(self.adj_list.keys()):
            print(f"  {vertex}：{self.adj_list[vertex]}")

class GraphTraversal:
    """圖的走訪演算法實作"""
    
    # --- 深度優先搜尋 (DFS) ---
    @staticmethod
    def dfs_recursive(graph, start_node, visited=None):
        """遞迴實作 DFS"""
        if visited is None: visited = set()
        visited.add(start_node)
        result = [start_node]
        
        neighbors = graph.adj_list.get(start_node, [])
        neighbor_nodes = [v if isinstance(v, int) else v[0] for v in neighbors]
        
        for neighbor in neighbor_nodes:
            if neighbor not in visited:
                result.extend(GraphTraversal.dfs_recursive(graph, neighbor, visited))
        return result

    @staticmethod
    def dfs_iterative(graph, start_node):
        """迭代實作 DFS"""
        visited = set()
        stack = [start_node]
        result = []
        
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                result.append(curr)
                
                neighbors = graph.adj_list.get(curr, [])
                neighbor_nodes = [v if isinstance(v, int) else v[0] for v in neighbors]
                
                # 反向推入以保持順序
                for neighbor in reversed(neighbor_nodes):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return result

    @staticmethod
    def dfs_all_vertices(graph):
        """對所有頂點進行 DFS (處理非連通圖)"""
        visited = set()
        result = []
        for vertex in sorted(graph.get_vertices()):
            if vertex not in visited:
                result.extend(GraphTraversal.dfs_recursive(graph, vertex, visited))
        return result

    # --- 廣度優先搜尋 (BFS) ---
    @staticmethod
    def bfs(graph, start_node):
        """實作 BFS"""
        visited = {start_node}
        queue = collections.deque([start_node])
        result = []
        
        while queue:
            curr = queue.popleft()
            result.append(curr)
            
            neighbors = graph.adj_list.get(curr, [])
            neighbor_nodes = [v if isinstance(v, int) else v[0] for v in neighbors]
            
            for neighbor in neighbor_nodes:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

    @staticmethod
    def bfs_all_vertices(graph):
        """對所有頂點進行 BFS (處理非連通圖)"""
        visited = set()
        result = []
        for vertex in sorted(graph.get_vertices()):
            if vertex not in visited:
                # 這裡直接呼叫 bfs 並更新全域 visited
                component = GraphTraversal.bfs(graph, vertex)
                result.extend(component)
                visited.update(component)
        return result

    @staticmethod
    def bfs_by_level(graph, start_node):
        """按層級分組的 BFS"""
        visited = {start_node}
        queue = collections.deque([start_node])
        levels = []
        
        while queue:
            level_size = len(queue)
            level_nodes = []
            for _ in range(level_size):
                curr = queue.popleft()
                level_nodes.append(curr)
                
                neighbors = graph.adj_list.get(curr, [])
                neighbor_nodes = [v if isinstance(v, int) else v[0] for v in neighbors]
                
                for neighbor in neighbor_nodes:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            levels.append(level_nodes)
        return levels

    # --- 路徑查找與環檢測 ---
    @staticmethod
    def find_path_dfs(graph, start, end, visited=None):
        """使用 DFS 尋找路徑"""
        if visited is None: visited = set()
        if start == end: return [start]
        
        visited.add(start)
        neighbors = graph.adj_list.get(start, [])
        neighbor_nodes = [v if isinstance(v, int) else v[0] for v in neighbors]
        
        for neighbor in neighbor_nodes:
            if neighbor not in visited:
                path = GraphTraversal.find_path_dfs(graph, neighbor, end, visited)
                if path:
                    return [start] + path
        return None

    @staticmethod
    def find_shortest_path_bfs(graph, start, end):
        """使用 BFS 尋找最短路徑"""
        if start == end: return [start]
        visited = {start}
        queue = collections.deque([(start, [start])])
        
        while queue:
            curr, path = queue.popleft()
            neighbors = graph.adj_list.get(curr, [])
            neighbor_nodes = [v if isinstance(v, int) else v[0] for v in neighbors]
            
            for neighbor in neighbor_nodes:
                if neighbor not in visited:
                    if neighbor == end:
                        return path + [neighbor]
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    @staticmethod
    def has_cycle(graph):
        """檢測無向圖中是否有環"""
        visited = set()
        def dfs_cycle(u, parent):
            visited.add(u)
            neighbors = graph.adj_list.get(u, [])
            neighbor_nodes = [v if isinstance(v, int) else v[0] for v in neighbors]
            for v in neighbor_nodes:
                if v not in visited:
                    if dfs_cycle(v, u): return True
                elif v != parent:
                    return True
            return False

        for node in graph.get_vertices():
            if node not in visited:
                if dfs_cycle(node, None): return True
        return False

# 示例用法
if __name__ == "__main__":
    print("=" * 60)
    print("圖的走訪：DFS 與 BFS 示例")
    print("=" * 60)
    
    g = Graph(6)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(1, 2)
    g.add_edge(2, 5)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    
    print("圖的結構：")
    print("    0 --- 1 --- 2")
    print("    |           |")
    print("    3 --- 4 --- 5")
    print()
    g.display()
    print()
    
    print("深度優先搜尋 (DFS):")
    print(f"  DFS 從頂點 0 (遞迴): {GraphTraversal.dfs_recursive(g, 0)}")
    print(f"  DFS 從頂點 0 (迭代): {GraphTraversal.dfs_iterative(g, 0)}")
    
    print("\n廣度優先搜尋 (BFS):")
    print(f"  BFS 從頂點 0: {GraphTraversal.bfs(g, 0)}")
    print(f"  BFS 按層級:")
    for i, level in enumerate(GraphTraversal.bfs_by_level(g, 0)):
        print(f"    第 {i} 層: {level}")
    
    print("\n路徑查找:")
    print(f"  從 0 到 5 的路徑 (DFS): {GraphTraversal.find_path_dfs(g, 0, 5)}")
    print(f"  從 0 到 5 的最短路徑 (BFS): {GraphTraversal.find_shortest_path_bfs(g, 0, 5)}")
    
    print("\n環檢測:")
    print(f"  圖中是否有環: {GraphTraversal.has_cycle(g)}")
    
    print("\n非連通圖示例:")
    g2 = Graph(6)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(3, 4)
    g2.add_edge(4, 5)
    print("  DFS 所有頂點: ", GraphTraversal.dfs_all_vertices(g2))
    print("  BFS 所有頂點: ", GraphTraversal.bfs_all_vertices(g2))
