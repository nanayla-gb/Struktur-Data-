"""
Jawaban Tugas: Sorting Lanjutan + Binary Tree (Expression HeapSort)
"""

import math
from typing import List, Optional
from collections import deque


# ============================================================
# BAGIAN 1: AdvancedSorter
# ============================================================

class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return f"ListNode({self.data})"


class AdvancedSorter:
    def __init__(self):
        pass

    # --------------------------------------------------------
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # --------------------------------------------------------
    def sort_array(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)  # Satu array sementara, dialokasi sekali
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        if first >= last:
            return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        """
        Menggabungkan dua virtual sublist yang bersebelahan.
        arr[left_start..mid] dan arr[mid+1..right_end]
        Gunakan tmp_array sebagai penyimpanan sementara (STABLE: <= dari kiri).
        """
        a = left_start       # pointer sublist kiri
        b = mid + 1          # pointer sublist kanan
        k = left_start       # pointer ke tmp_array

        while a <= mid and b <= right_end:
            # STABLE: jika sama, ambil dari kiri dulu (<=)
            if arr[a] <= arr[b]:
                tmp_array[k] = arr[a]
                a += 1
            else:
                tmp_array[k] = arr[b]
                b += 1
            k += 1

        # Sisa elemen kiri
        while a <= mid:
            tmp_array[k] = arr[a]
            a += 1
            k += 1

        # Sisa elemen kanan
        while b <= right_end:
            tmp_array[k] = arr[b]
            b += 1
            k += 1

        # Salin kembali dari tmp_array ke arr
        for i in range(left_start, right_end + 1):
            arr[i] = tmp_array[i]

    # --------------------------------------------------------
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # --------------------------------------------------------
    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        right_head = self._split_linked_list(head)
        left_head = head
        left_sorted  = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Fast-Slow pointer:
        - midPoint  bergerak 1 langkah per iterasi
        - curNode   bergerak 2 langkah per iterasi
        Saat curNode mencapai akhir, midPoint berada di tengah.
        """
        midPoint = head
        curNode  = head.next

        while curNode is not None and curNode.next is not None:
            midPoint = midPoint.next
            curNode  = curNode.next.next

        right_head       = midPoint.next
        midPoint.next    = None   # putus list menjadi dua bagian
        return right_head

    def _merge_linked_lists(self,
                             listA: Optional[ListNode],
                             listB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Merge dengan dummy node & tail reference.
        Tidak mengalokasi node baru — hanya mengubah pointer .next.
        STABLE: jika sama, ambil dari listA lebih dulu.
        """
        dummy = ListNode(0)   # satu dummy node statis per merge (diizinkan)
        tail  = dummy

        while listA is not None and listB is not None:
            # STABLE: <= ambil kiri dulu
            if listA.data <= listB.data:
                tail.next = listA
                listA     = listA.next
            else:
                tail.next = listB
                listB     = listB.next
            tail = tail.next

        # Sambung sisa
        tail.next = listA if listA is not None else listB

        return dummy.next

    # --------------------------------------------------------
    # 3. QUICK SORT PARTITION (Median-of-Three Pivot)
    # --------------------------------------------------------
    def quick_sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        n = len(arr)
        self._quick_sort_recursive(arr, 0, n - 1, depth=0, n=n)
        return arr

    def _quick_sort_recursive(self, arr, first, last, depth, n):
        if first >= last:
            return

        # Fallback ke Merge Sort jika kedalaman rekursi terlalu dalam
        limit = int(2 * math.log2(max(n, 2)))
        if depth > limit:
            # Ekstrak subarray, sort dengan merge sort, kembalikan
            sub = arr[first:last + 1]
            self.sort_array(sub)
            arr[first:last + 1] = sub
            return

        pivot_idx = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first, pivot_idx - 1, depth + 1, n)
        self._quick_sort_recursive(arr, pivot_idx + 1, last, depth + 1, n)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Median-of-Three pivot:
        1. Bandingkan arr[first], arr[mid], arr[last]
        2. Tukar median ke posisi arr[first]
        3. Jalankan partisi standar (in-place)
        """
        mid = (first + last) // 2

        # Urutkan tiga kandidat sehingga median ada di arr[mid]
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]
        # Kini arr[first] <= arr[mid] <= arr[last]
        # median = arr[mid] → pindahkan ke arr[first] sebagai pivot
        arr[first], arr[mid] = arr[mid], arr[first]

        pivot = arr[first]
        left  = first + 1
        right = last

        while True:
            # Gerak left ke kanan selama arr[left] <= pivot
            while left <= right and arr[left] <= pivot:
                left += 1
            # Gerak right ke kiri selama arr[right] > pivot
            while right >= left and arr[right] > pivot:
                right -= 1
            if left > right:
                break
            arr[left], arr[right] = arr[right], arr[left]

        # Tempatkan pivot pada posisi akhirnya
        arr[first], arr[right] = arr[right], arr[first]
        return right


# ============================================================
# BAGIAN 2: ExprHeapSorter
# ============================================================

class ExprHeapSorter:
    def __init__(self, expr_str: str):
        self.expr   = expr_str
        self.values = []

    # --------------------------------------------------------
    # Expression Tree Builder & Evaluator
    # --------------------------------------------------------
    def parse_and_evaluate(self) -> List[int]:
        """Membangun pohon ekspresi, evaluasi, kembalikan list nilai integer."""
        # Tokenize: pisahkan karakter bermakna
        tokens = deque()
        i = 0
        s = self.expr.replace(' ', '')
        while i < len(s):
            if s[i].isdigit():
                j = i
                while j < len(s) and s[j].isdigit():
                    j += 1
                tokens.append(s[i:j])
                i = j
            elif s[i] in '()+−-*/':
                tokens.append(s[i])
                i += 1
            else:
                i += 1  # abaikan karakter tidak dikenal

        root = self._build_tree(tokens)
        result = self._eval_tree(root)
        self.values = [result]
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Rekursif membangun pohon ekspresi dari antrian token.
        Pola: '(' → bangun_kiri → operator → bangun_kanan → ')'
        Operand langsung → node daun.
        """
        if not tokens:
            return None

        token = tokens.popleft()

        if token == '(':
            # Bangun subtree kiri
            left_node = self._build_tree(tokens)
            # Ambil operator
            operator  = tokens.popleft() if tokens else None
            # Bangun subtree kanan
            right_node = self._build_tree(tokens)
            # Konsumsi ')'
            if tokens and tokens[0] == ')':
                tokens.popleft()
            return {'val': operator, 'left': left_node, 'right': right_node}
        else:
            # Token adalah operand (angka)
            try:
                return {'val': int(token), 'left': None, 'right': None}
            except ValueError:
                raise ValueError(f"Token tidak valid: '{token}'")

    def _eval_tree(self, node: Optional[dict]):
        """
        Evaluasi postorder: kiri → kanan → operator.
        Handle division by zero.
        """
        if node is None:
            raise ValueError("Node kosong saat evaluasi")

        # Node daun (operand)
        if node['left'] is None and node['right'] is None:
            return node['val']

        left_val  = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])
        op        = node['val']

        if op == '+':
            return left_val + right_val
        elif op in ('-', '−'):
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("Division by zero")
            return left_val / right_val
        else:
            raise ValueError(f"Operator tidak dikenal: '{op}'")

    # --------------------------------------------------------
    # In-Place HeapSort
    # --------------------------------------------------------
    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """Mengurutkan array secara ascending menggunakan in-place heapsort."""
        n = len(arr)
        if n <= 1:
            return arr

        # Fase 1: Bangun max-heap dari daun ke akar
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # Fase 2: Ekstrak elemen max satu per satu
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]   # pindah max ke akhir
            self._sift_down(arr, end, 0)           # pulihkan heap

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Sift-down untuk memulihkan max-heap property.
        Loop selama ada anak yang lebih besar dari node saat ini.
        """
        while True:
            largest = idx
            left    = 2 * idx + 1
            right   = 2 * idx + 2

            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            if largest == idx:
                break   # Heap property terpenuhi

            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest

    # --------------------------------------------------------
    # Complete Tree Validator
    # --------------------------------------------------------
    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Validasi bahwa array memenuhi properti complete binary tree.
        Pada complete binary tree, jika ada node di indeks i:
        - Anak kiri  ada di 2*i+1
        - Anak kanan ada di 2*i+2
        Tidak boleh ada "lubang" (node kosong di tengah level).
        Cara: setelah menemukan None pertama, semua node berikutnya harus None.
        """
        n = len(arr)
        if n == 0:
            return True

        found_none = False
        for i in range(n):
            left  = 2 * i + 1
            right = 2 * i + 2

            if left < n:
                if found_none:
                    return False   # Ada node setelah None → tidak complete
            else:
                found_none = True  # Node kiri tidak ada → mulai zona None

            if right < n:
                if found_none:
                    return False
            else:
                found_none = True

        return True


# ============================================================
# HELPER: Tampilkan Linked List
# ============================================================
def list_to_linkedlist(items):
    if not items:
        return None
    head = ListNode(items[0])
    cur  = head
    for v in items[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head

def linkedlist_to_list(head):
    result = []
    cur = head
    while cur:
        result.append(cur.data)
        cur = cur.next
    return result


# ============================================================
# DEMO & UJI COBA
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  BAGIAN 1: AdvancedSorter")
    print("=" * 55)

    sorter = AdvancedSorter()

    # --- Array Merge Sort ---
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"\n[Merge Sort Array]")
    print(f"  Input : {arr}")
    result = sorter.sort_array(arr[:])
    print(f"  Output: {result}")

    # Stabilitas: elemen sama
    arr2 = [4, 2, 4, 1, 3, 2]
    print(f"\n[Merge Sort - Stabilitas]")
    print(f"  Input : {arr2}")
    print(f"  Output: {sorter.sort_array(arr2[:])}")

    # --- Linked List Merge Sort ---
    print(f"\n[Linked List Merge Sort]")
    data = [5, 2, 8, 1, 9, 3]
    head = list_to_linkedlist(data)
    print(f"  Input : {data}")
    sorted_head = sorter.sort_linked_list(head)
    print(f"  Output: {linkedlist_to_list(sorted_head)}")

    # --- Quick Sort ---
    arr3 = [64, 34, 25, 12, 22, 11, 90]
    print(f"\n[Quick Sort - Median-of-Three]")
    print(f"  Input : {arr3}")
    print(f"  Output: {sorter.quick_sort(arr3[:])}")

    # Worst case: already sorted descending
    arr4 = list(range(20, 0, -1))
    print(f"\n[Quick Sort - Descending (worst-case test)]")
    print(f"  Input : {arr4}")
    print(f"  Output: {sorter.quick_sort(arr4[:])}")

    print("\n" + "=" * 55)
    print("  BAGIAN 2: ExprHeapSorter")
    print("=" * 55)

    # --- Expression Tree ---
    expr = "((8*5)+(9/(7-4)))"
    ehs = ExprHeapSorter(expr)
    print(f"\n[Expression Tree Evaluator]")
    print(f"  Ekspresi: {expr}")
    try:
        val = ehs.parse_and_evaluate()
        print(f"  Hasil   : {val[0]}")   # 8*5=40, 7-4=3, 9/3=3, 40+3=43
    except ValueError as e:
        print(f"  Error: {e}")

    # --- In-Place HeapSort ---
    data2 = [43, 3, 9, 82, 10, 27, 38, 15]
    ehs2  = ExprHeapSorter("")
    print(f"\n[HeapSort In-Place]")
    print(f"  Input : {data2}")
    sorted_data = ehs2.heapsort_inplace(data2[:])
    print(f"  Output: {sorted_data}")

    # --- Complete Tree Validator ---
    print(f"\n[Complete Tree Validator]")
    complete     = [1, 2, 3, 4, 5, 6]
    not_complete = [1, 2, 3, None, 5, 6]
    arr_only     = [10, 20, 30, 40, 50]
    print(f"  [1,2,3,4,5,6]   → Complete: {ehs2.is_complete_tree(complete)}")
    print(f"  [10,20,30,40,50]→ Complete: {ehs2.is_complete_tree(arr_only)}")

    # Sorted array sebagai complete binary tree (setelah heapsort)
    print(f"  Sorted {sorted_data} → Complete: {ehs2.is_complete_tree(sorted_data)}")

    # --- Division by zero test ---
    print(f"\n[Division by Zero Test]")
    ehs3 = ExprHeapSorter("((8*5)+(9/(7-7)))")
    try:
        ehs3.parse_and_evaluate()
    except ValueError as e:
        print(f"  Tertangkap error: {e}")

    print("\n✅ Semua modul berjalan sukses.")