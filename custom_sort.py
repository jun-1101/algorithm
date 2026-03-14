import time
import random

def insertion_sort(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge(arr, left, mid, right):
    len1 = mid - left + 1
    len2 = right - mid

    left_half = [0] * len1
    right_half = [0] * len2

    for i in range(len1):
        left_half[i] = arr[left + i]
    for i in range(len2):
        right_half[i] = arr[mid + 1 + i]

    i, j, k = 0, 0, left

    while i < len1 and j < len2:
        if left_half[i] <= right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len2:
        arr[k] = right_half[j]
        j += 1
        k += 1

def hybrid_merge_sort(arr, left, right, threshold=10):
    if left < right:
        if right - left + 1 <= threshold:
            insertion_sort(arr, left, right)
        else:
            mid = (left + right) // 2
            hybrid_merge_sort(arr, left, mid, threshold)
            hybrid_merge_sort(arr, mid + 1, right, threshold)
            merge(arr, left, mid, right)

def generate_random_array(size):
    return [random.randint(0, size * 10) for _ in range(size)]

if __name__ == "__main__":
    input_sizes = [100, 1000, 5000, 10000, 20000, 50000, 100000] 
    
    print("Assignment 3: Custom Sorting Algorithm (Hybrid Merge Sort) Time Complexity Analysis\n")
    print(f"{'Input Size':<15} | {'Running Time (ms)':<20}")
    print("---------------------------------------------------")

    for size in input_sizes:
        original_array = generate_random_array(size)
        arr_to_sort = original_array.copy()

        start_time = time.time()
        hybrid_merge_sort(arr_to_sort, 0, len(arr_to_sort) - 1)
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000

        print(f"{size:<15} | {duration_ms:<20.4f}")


