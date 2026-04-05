import math

class DivideAndConquer:
    """分治策略演算法實作"""
    
    # --- 合併排序 (Merge Sort) ---
    @staticmethod
    def merge_sort(arr):
        """實作合併排序"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = DivideAndConquer.merge_sort(arr[:mid])
        right = DivideAndConquer.merge_sort(arr[mid:])
        
        return DivideAndConquer._merge(left, right)

    @staticmethod
    def _merge(left, right):
        """合併兩個已排序的陣列"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # --- 二分搜尋 (Binary Search) ---
    @staticmethod
    def binary_search_recursive(arr, target, low, high):
        """遞迴實作二分搜尋"""
        if low > high:
            return -1
        
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return DivideAndConquer.binary_search_recursive(arr, target, low, mid - 1)
        else:
            return DivideAndConquer.binary_search_recursive(arr, target, mid + 1, high)

    @staticmethod
    def binary_search_iterative(arr, target):
        """迭代實作二分搜尋"""
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] > target:
                high = mid - 1
            else:
                low = mid + 1
        return -1

    # --- 逆序對計算 (Inversion Count) ---
    @staticmethod
    def count_inversions(arr):
        """計算陣列中的逆序對數量"""
        def merge_and_count(temp_arr, left, mid, right):
            i = left    # 左子陣列索引
            j = mid + 1 # 右子陣列索引
            k = left    # 合併後陣列索引
            inv_count = 0
            
            while i <= mid and j <= right:
                if temp_arr[i] <= temp_arr[j]:
                    i += 1
                else:
                    # 如果左側元素大於右側元素，則存在逆序對
                    # 且左側剩餘的所有元素都與該右側元素構成逆序對
                    inv_count += (mid - i + 1)
                    j += 1
                k += 1
            return inv_count

        def sort_and_count(temp_arr, left, right):
            inv_count = 0
            if left < right:
                mid = (left + right) // 2
                inv_count += sort_and_count(temp_arr, left, mid)
                inv_count += sort_and_count(temp_arr, mid + 1, right)
                inv_count += merge_and_count(temp_arr, left, mid, right)
                # 為了簡化，這裡不進行實際排序，僅計算數量
                temp_arr[left:right+1] = sorted(temp_arr[left:right+1])
            return inv_count

        return sort_and_count(arr[:], 0, len(arr) - 1)

    # --- 最接近點對 (Closest Pair of Points) ---
    @staticmethod
    def closest_pair(points):
        """尋找平面上最接近的點對"""
        def dist(p1, p2):
            return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

        def closest_recursive(px, py):
            n = len(px)
            if n <= 3:
                min_d = float('inf')
                pair = None
                for i in range(n):
                    for j in range(i + 1, n):
                        d = dist(px[i], px[j])
                        if d < min_d:
                            min_d = d
                            pair = (px[i], px[j])
                return pair, min_d

            mid_idx = n // 2
            mid_point = px[mid_idx]
            
            py_left = [p for p in py if p[0] <= mid_point[0]]
            py_right = [p for p in py if p[0] > mid_point[0]]
            
            (pair_l, dist_l) = closest_recursive(px[:mid_idx], py_left)
            (pair_r, dist_r) = closest_recursive(px[mid_idx:], py_right)
            
            if dist_l < dist_r:
                best_pair, min_dist = pair_l, dist_l
            else:
                best_pair, min_dist = pair_r, dist_r
                
            strip = [p for p in py if abs(p[0] - mid_point[0]) < min_dist]
            
            for i in range(len(strip)):
                j = i + 1
                while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist:
                    d = dist(strip[i], strip[j])
                    if d < min_dist:
                        min_dist = d
                        best_pair = (strip[i], strip[j])
                    j += 1
            return best_pair, min_dist

        px = sorted(points, key=lambda p: p[0])
        py = sorted(points, key=lambda p: p[1])
        return closest_recursive(px, py)

# 示例用法
if __name__ == "__main__":
    print("=" * 60)
    print("分治策略演算法示例")
    print("=" * 60)
    
    # 測試合併排序
    print("\n合併排序 (Merge Sort):")
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"  原始陣列: {arr}")
    sorted_arr = DivideAndConquer.merge_sort(arr)
    print(f"  排序後: {sorted_arr}")
    
    # 測試二分搜尋
    print("\n二分搜尋 (Binary Search):")
    search_arr = [2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78]
    target = 23
    print(f"  陣列: {search_arr}")
    print(f"  搜尋目標: {target}")
    idx_rec = DivideAndConquer.binary_search_recursive(search_arr, target, 0, len(search_arr)-1)
    idx_ite = DivideAndConquer.binary_search_iterative(search_arr, target)
    print(f"  遞迴結果索引: {idx_rec}")
    print(f"  迭代結果索引: {idx_ite}")
    
    # 測試逆序對計算
    print("\n逆序對計算 (Inversion Count):")
    inv_arr = [2, 4, 1, 3, 5]
    print(f"  陣列: {inv_arr}")
    count = DivideAndConquer.count_inversions(inv_arr)
    print(f"  逆序對數量: {count}")
    
    # 測試最接近點對
    print("\n最接近點對 (Closest Pair):")
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    pair, distance = DivideAndConquer.closest_pair(points)
    print(f"  點集合: {points}")
    print(f"  最接近點對: {pair}")
    print(f"  距離: {distance:.2f}")
