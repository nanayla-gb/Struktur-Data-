def insertionSortDescending(theSeq):
    n = len(theSeq)
    for i in range(1, n):
        value = theSeq[i]
        pos = i
        
        # Ganti tanda value < theSeq[pos-1] menjadi value > theSeq[pos-1]
        while pos > 0 and value > theSeq[pos - 1]:
            theSeq[pos] = theSeq[pos - 1]
            pos -= 1
            
        theSeq[pos] = value
    return theSeq

# Uji Coba
data = [10, 51, 2, 18, 4, 31]
print("Soal 4 (Descending):", insertionSortDescending(data))
# Output: [51, 31, 18, 10, 4, 2]