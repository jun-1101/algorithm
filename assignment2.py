import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char  = char
        self.freq  = freq
        self.left  = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.root       = None
        self.code_table = {}   

    def build_tree(self, text):
        
        freq = Counter(text)

        heap = [HuffmanNode(char, f) for char, f in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left  = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left  = left
            merged.right = right
            heapq.heappush(heap, merged)

        self.root = heapq.heappop(heap)
        self._assign_codes(self.root, "")

    def _assign_codes(self, node, code):
        
        if node is None:
            return
        if node.char is not None:   
            self.code_table[node.char] = code if code else "0"
            return
        self._assign_codes(node.left,  code + "0")
        self._assign_codes(node.right, code + "1")

    def encode(self, text):
        
        return "".join(self.code_table[ch] for ch in text)

    def decode(self, bits):
        
        result = []
        node = self.root
        for bit in bits:
            node = node.left if bit == "0" else node.right
            if node.char is not None:   
                result.append(node.char)
                node = self.root
        return "".join(result)

    def print_codes(self):
        print("Huffman Codes:")
        for char, code in sorted(self.code_table.items()):
            print(f"  '{char}' : {code}")

    def print_time_complexity(self):
        print("Huffman Coding Time Complexity:")
        print("  Build heap (n unique chars)  : O(n)")
        print("  Merge loop (n-1 times)       : O(n log n)")
        print("  Assign codes (tree traversal): O(n)")
        print("  Encode string (length m)     : O(m)")
        print("  Decode bits   (length m)     : O(m)")
        print("  Overall (build)              : O(n log n)")


if __name__ == "__main__":
    text = "abracadabra"
    print("Original text :", text)

    hc = HuffmanCoding()
    hc.build_tree(text)

    hc.print_codes()

    encoded = hc.encode(text)
    print("\nEncoded :", encoded)
    print("Encoded length :", len(encoded), "bits")
    print("Original length:", len(text) * 8, "bits (8-bit ASCII)")

    decoded = hc.decode(encoded)
    print("\nDecoded :", decoded)
    print("Match   :", decoded == text)

    print()
    hc.print_time_complexity()
