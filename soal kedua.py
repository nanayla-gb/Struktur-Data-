class Set:
    def __init__(self):
        self._theElements = list()

    def __len__(self):
        return len(self._theElements)

    def __contains__(self, element):
        # Menggunakan Binary Search karena list terurut
        low = 0
        high = len(self._theElements) - 1
        while low <= high:
            mid = (low + high) // 2
            if self._theElements[mid] == element:
                return True
            elif element < self._theElements[mid]:
                high = mid - 1
            else:
                low = mid + 1
        return False

    def union(self, otherSet):
        """
        Soal 5: Operasi Union yang efisien (O(n)) 
        menggunakan teknik merge pada dua sorted list.
        """
        newSet = Set()
        a = 0
        b = 0
        
        # Ambil referensi list agar kode lebih rapi
        listA = self._theElements
        listB = otherSet._theElements
        
        # Iterasi melalui kedua list secara bersamaan
        while a < len(listA) and b < len(listB):
            if listA[a] < listB[b]:
                newSet._theElements.append(listA[a])
                a += 1
            elif listA[a] > listB[b]:
                newSet._theElements.append(listB[b])
                b += 1
            else: # Jika elemen sama, masukkan satu kali saja (syarat Set)
                newSet._theElements.append(listA[a])
                a += 1
                b += 1
                
        # Jika ada sisa elemen di listA
        while a < len(listA):
            newSet._theElements.append(listA[a])
            a += 1
            
        # Jika ada sisa elemen di listB
        while b < len(listB):
            newSet._theElements.append(listB[b])
            b += 1
            
        return newSet

# --- Contoh Penggunaan ---
set1 = Set()
set1._theElements = [2, 8, 15, 23, 37] # Simulasi sorted list

set2 = Set()
set2._theElements = [4, 6, 15, 20]     # Simulasi sorted list

hasil = set1.union(set2)
print("Hasil Union:", hasil._theElements)
# Output: [2, 4, 6, 8, 15, 20, 23, 37]