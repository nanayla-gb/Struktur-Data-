"""
Labirin Random + Pencari Jalan Otomatis
Stack + Backtracking - Struktur Data Bab 7
"""

import random, sys, time
sys.setrecursionlimit(10000)

ROWS, COLS = 19, 25

# ── STACK ──────────────────────────────────────────────
class Stack:
    def __init__(self):       self._d = []
    def isEmpty(self):        return len(self._d) == 0
    def push(self, item):     self._d.append(item)
    def pop(self):            return self._d.pop()
    def peek(self):           return self._d[-1]

# ── GENERATE LABIRIN RANDOM (DFS Recursive Backtracker) ─
def generate(rows, cols):
    grid = [[1]*cols for _ in range(rows)]  # 1=dinding, 0=jalan

    def carve(r, c):
        grid[r][c] = 0
        dirs = [(-2,0),(2,0),(0,-2),(0,2)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 1 <= nr < rows-1 and 1 <= nc < cols-1 and grid[nr][nc] == 1:
                grid[r+dr//2][c+dc//2] = 0
                carve(nr, nc)

    carve(1, 1)
    # exit: cari sel terbuka paling kanan bawah
    er, ec = rows-2, cols-2
    while grid[er][ec] == 1 and er > 1:
        ec -= 1
        if ec < 1: ec = cols-2; er -= 1
    return grid, 1, 1, er, ec

# ── SOLVE: Stack + Backtracking ─────────────────────────
def solve(grid, sr, sc, er, ec, rows, cols):
    tokens = [[None]*cols for _ in range(rows)]
    stack  = Stack()
    stack.push((sr, sc))
    tokens[sr][sc] = 'x'
    history = []  # simpan snapshot tiap langkah

    while not stack.isEmpty():
        r, c = stack.peek()
        history.append((r, c, [row[:] for row in tokens], list(stack._d)))

        if r == er and c == ec:
            return True, tokens, history

        moved = False
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0 and tokens[nr][nc] is None:
                tokens[nr][nc] = 'x'
                stack.push((nr, nc))
                moved = True
                break

        if not moved:
            tokens[r][c] = 'o'
            stack.pop()

    return False, tokens, history

# ── TAMPILAN ─────────────────────────────────────────────
R  = '\033[0m'
WALL  = '\033[90m██\033[0m'
OPEN  = '  '
PATH  = '\033[92m::\033[0m'   # jalur - hijau
TRIED = '\033[91m··\033[0m'   # buntu - merah
START = '\033[93mSS\033[0m'   # kuning
EXIT  = '\033[96mEE\033[0m'   # cyan
HEAD  = '\033[95m>>\033[0m'   # posisi sekarang - magenta

def draw(grid, tokens, rows, cols, sr, sc, er, ec, head=None):
    print('\033[H', end='')  # cursor ke atas (clear screen in-place)
    for r in range(rows):
        row = ''
        for c in range(cols):
            if   (r,c) == (sr,sc): row += START
            elif (r,c) == (er,ec): row += EXIT
            elif (r,c) == head:    row += HEAD
            elif grid[r][c] == 1:  row += WALL
            elif tokens[r][c]=='x':row += PATH
            elif tokens[r][c]=='o':row += TRIED
            else:                  row += OPEN
        print(row)

# ── MAIN ─────────────────────────────────────────────────
def main():
    while True:
        print('\033[2J\033[H', end='')  # clear screen
        print("╔══════════════════════════════════════╗")
        print("║  LABIRIN RANDOM - Stack + Backtrack  ║")
        print("║  Struktur Data | Bab 7               ║")
        print("╚══════════════════════════════════════╝")
        print()
        print(f"\033[92m::\033[0m = Jalur  \033[91m··\033[0m = Jalan Buntu  "
              f"\033[95m>>\033[0m = Posisi kini  \033[93mSS\033[0m = Start  \033[96mEE\033[0m = Exit")
        print()

        # ukuran
        try:
            r = int(input("Jumlah baris (ganjil, default 19): ").strip() or "19")
            c = int(input("Jumlah kolom (ganjil, default 25): ").strip() or "25")
        except ValueError:
            r, c = 19, 25
        if r%2==0: r+=1
        if c%2==0: c+=1
        r = max(7, min(35, r))
        c = max(7, min(51, c))

        delay_map = {'1':0.15,'2':0.05,'3':0.01,'4':0.001,'5':0}
        print("\nKecepatan animasi:")
        print("  1=Sangat lambat  2=Lambat  3=Normal  4=Cepat  5=Instan")
        spd = input("Pilih [1-5] (default 3): ").strip() or "3"
        delay = delay_map.get(spd, 0.01)

        # generate
        print("\nGenerating labirin...")
        grid, sr, sc, er, ec = generate(r, c)

        # tampil labirin awal
        empty_tok = [[None]*c for _ in range(r)]
        print('\033[2J\033[H', end='')
        print("── LABIRIN AWAL ──────────────────────────────")
        draw(grid, empty_tok, r, c, sr, sc, er, ec)
        input("\nTekan Enter untuk mulai mencari jalur...")

        # solve
        found, tokens, history = solve(grid, sr, sc, er, ec, r, c)

        # animasi
        print('\033[2J\033[H', end='')
        if delay > 0:
            for i, (hr, hc, snap_tok, snap_stk) in enumerate(history):
                draw(grid, snap_tok, r, c, sr, sc, er, ec, head=(hr,hc))
                print(f"\nStep: {i+1:4d} | Stack size: {len(snap_stk):3d} | "
                      f"Jalur: {sum(v=='x' for row in snap_tok for v in row):3d} | "
                      f"Buntu: {sum(v=='o' for row in snap_tok for v in row):3d}")
                if delay > 0:
                    time.sleep(delay)
        else:
            draw(grid, tokens, r, c, sr, sc, er, ec)

        # hasil akhir
        jalur  = sum(v=='x' for row in tokens for v in row)
        buntu  = sum(v=='o' for row in tokens for v in row)
        total  = len(history)

        print(f"\n── HASIL ──────────────────────────────────────")
        if found:
            print(f"  ✅ JALUR DITEMUKAN!")
            print(f"  📍 Start         : ({sr}, {sc})")
            print(f"  🚪 Exit          : ({er}, {ec})")
            print(f"  🟢 Panjang jalur : {jalur} langkah")
            print(f"  🔴 Jalan buntu   : {buntu} sel")
            print(f"  🔢 Total steps   : {total}")
        else:
            print("  ❌ Tidak ada jalur yang ditemukan!")

        print(f"\n── CARA KERJA STACK + BACKTRACKING ───────────")
        print("  1. push(start) → tandai jalur 'x'")
        print("  2. peek() → cek posisi teratas stack")
        print("  3. Exit ketemu? → return True ✅")
        print("  4. Ada tetangga? → push(), tandai 'x'")
        print("  5. Jalan buntu? → tandai 'o', pop() ← BACKTRACK")
        print("  6. Stack kosong? → return False ❌")

        lagi = input("\nGenerate labirin baru? (y/n): ").strip().lower()
        if lagi != 'y':
            break

    print("\nSampai jumpa! 👋")

if __name__ == '__main__':
    main()