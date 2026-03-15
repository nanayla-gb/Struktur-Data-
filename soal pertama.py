class SortedList:
    def __init__(self):
        self._theItems = []

    def __len__(self):
        return len(self._theItems)

    def __contains__(self, target):
        """Soal 5a: Menggunakan Binary Search untuk mengecek data"""
        low = 0
        high = len(self._theItems) - 1
        while low <= high:
            mid = (low + high) // 2
            if self._theItems[mid] == target:
                return True
            elif target < self._theItems[mid]:
                high = mid - 1
            else:
                low = mid + 1
        return False

    def add(self, item):
        """Soal 5b: Menambahkan item baru di posisi yang tepat agar tetap terurut"""
        # Cari posisi index yang tepat menggunakan logika Binary Search
        low = 0
        high = len(self._theItems) - 1
        while low <= high:
            mid = (low + high) // 2
            if item < self._theItems[mid]:
                high = mid - 1
            else:
                low = mid + 1
        
        # Posisi sisip yang tepat adalah di indeks 'low'
        self._theItems.insert(low, item)

# --- Uji Coba Program ---
daftar = SortedList()
daftar.add(15)
daftar.add(2)
daftar.add(37)
daftar.add(8)
daftar.add(23)

print("Isi list (otomatis terurut):", daftar._theItems) 
# Output: [2, 8, 15, 23, 37]

print("Apakah ada angka 15?", 15 in daftar) # Output: True
print("Apakah ada angka 10?", 10 in daftar) # Output: False