def selectionSortDescending(theSeq):
    n = len(theSeq)
    for i in range(n - 1):
        # Anggap posisi i adalah yang terbesar sementara
        maxIndex = i 
        for j in range(i + 1, n):
            # Ganti tanda < menjadi > untuk mencari nilai terbesar
            if theSeq[j] > theSeq[maxIndex]:
                maxIndex = j
        
        # Tukar posisi jika ditemukan nilai yang lebih besar
        if maxIndex != i:
            theSeq[i], theSeq[maxIndex] = theSeq[maxIndex], theSeq[i]
    return theSeq

# Uji Coba
data = [10, 51, 2, 18, 4, 31]
print("Soal 3 (Descending):", selectionSortDescending(data))
# Output: [51, 31, 18, 10, 4, 2]