"""
GAME OF LIFE - Conway's Game of Life
Implementasi lengkap dalam satu file Python
Menggunakan ADT Array sesuai spesifikasi dokumen
"""

import time
import os
import random
import tkinter as tk
from tkinter import ttk

# ==================== ADT ARRAY ====================
class Array:
    """Kelas untuk merepresentasikan array satu dimensi"""
    
    def __init__(self, size):
        """
        Membuat array dengan ukuran tertentu
        Args:
            size: ukuran array (harus > 0)
        """
        if size <= 0:
            raise ValueError("Ukuran array harus lebih besar dari 0")
        self._size = size
        self._elements = [None] * size
    
    def length(self):
        """Mengembalikan panjang array"""
        return self._size
    
    def getitem(self, index):
        """Mengembalikan nilai pada indeks tertentu"""
        if index < 0 or index >= self._size:
            raise IndexError("Indeks di luar rentang array")
        return self._elements[index]
    
    def setitem(self, index, value):
        """Mengubah nilai pada indeks tertentu"""
        if index < 0 or index >= self._size:
            raise IndexError("Indeks di luar rentang array")
        self._elements[index] = value
    
    def clearing(self, value):
        """Mengosongkan array dengan nilai tertentu"""
        for i in range(self._size):
            self._elements[i] = value
    
    def __getitem__(self, index):
        """Operator [] untuk mendapatkan nilai"""
        return self.getitem(index)
    
    def __setitem__(self, index, value):
        """Operator [] untuk mengubah nilai"""
        self.setitem(index, value)
    
    def __len__(self):
        """Operator len() untuk mendapatkan panjang array"""
        return self.length()
    
    def __iter__(self):
        """Membuat iterator untuk array"""
        return ArrayIterator(self._elements)


class ArrayIterator:
    """Iterator untuk array"""
    
    def __init__(self, elements):
        self._elements = elements
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self._elements):
            value = self._elements[self._index]
            self._index += 1
            return value
        else:
            raise StopIteration


# ==================== ADT GRID ====================
class Grid:
    """Kelas untuk merepresentasikan grid 2D menggunakan Array"""
    
    def __init__(self, rows, cols):
        """
        Membuat grid dengan jumlah baris dan kolom tertentu
        Args:
            rows: jumlah baris
            cols: jumlah kolom
        """
        self._rows = rows
        self._cols = cols
        self._grid = Array(rows)
        for i in range(rows):
            self._grid[i] = Array(cols)
    
    def rows(self):
        """Mengembalikan jumlah baris"""
        return self._rows
    
    def cols(self):
        """Mengembalikan jumlah kolom"""
        return self._cols
    
    def getitem(self, row, col):
        """Mengembalikan nilai pada posisi (row, col)"""
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            raise IndexError("Posisi di luar rentang grid")
        return self._grid[row][col]
    
    def setitem(self, row, col, value):
        """Mengubah nilai pada posisi (row, col)"""
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            raise IndexError("Posisi di luar rentang grid")
        self._grid[row][col] = value
    
    def clear(self, value):
        """Mengosongkan grid dengan nilai tertentu"""
        for row in range(self._rows):
            for col in range(self._cols):
                self._grid[row][col] = value
    
    def __getitem__(self, row):
        """Mengembalikan baris tertentu"""
        return self._grid[row]
    
    def __setitem__(self, row, value):
        """Mengubah seluruh baris"""
        if len(value) != self._cols:
            raise ValueError("Jumlah kolom tidak sesuai")
        self._grid[row] = value
    
    def __str__(self):
        """Representasi string dari grid"""
        result = ""
        for row in range(self._rows):
            for col in range(self._cols):
                result += str(self._grid[row][col]) + " "
            result += "\n"
        return result


# ==================== GAME OF LIFE CORE ====================
class GameOfLife:
    """Kelas untuk mengimplementasikan Game of Life"""
    
    def __init__(self, rows, cols):
        """
        Inisialisasi Game of Life dengan ukuran grid tertentu
        Args:
            rows: jumlah baris grid
            cols: jumlah kolom grid
        """
        self.rows = rows
        self.cols = cols
        self.grid = Grid(rows, cols)
        self.generation = 0
        self._initialize_grid()
    
    def _initialize_grid(self):
        """Menginisialisasi grid dengan nilai 0 (mati)"""
        self.grid.clear(0)
    
    def set_cell(self, row, col, value):
        """Mengatur nilai sel pada posisi tertentu"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = value
    
    def get_cell(self, row, col):
        """Mendapatkan nilai sel pada posisi tertentu"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return 0
    
    def count_neighbors(self, row, col):
        """
        Menghitung jumlah tetangga hidup (bernilai 1) dari sel pada posisi (row, col)
        Tetangga adalah 8 sel di sekitar: vertikal, horizontal, dan diagonal
        """
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Lewati sel itu sendiri
                if i == 0 and j == 0:
                    continue
                
                r = row + i
                c = col + j
                
                # Pastikan posisi masih dalam batas grid
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    count += self.grid[r][c]
        
        return count
    
    def next_generation(self):
        """Menghitung generasi berikutnya berdasarkan aturan Game of Life"""
        # Buat grid baru untuk generasi berikutnya
        new_grid = Grid(self.rows, self.cols)
        
        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = self.count_neighbors(row, col)
                current_cell = self.grid[row][col]
                
                # Terapkan aturan Game of Life
                if current_cell == 1:  # Sel hidup
                    if neighbors < 2 or neighbors > 3:
                        # Aturan 2 & 3: Mati karena terisolasi atau kelebihan populasi
                        new_grid[row][col] = 0
                    else:
                        # Aturan 1: Tetap hidup
                        new_grid[row][col] = 1
                else:  # Sel mati
                    if neighbors == 3:
                        # Aturan 4: Kelahiran
                        new_grid[row][col] = 1
                    else:
                        new_grid[row][col] = 0
        
        # Update grid dengan generasi baru
        self.grid = new_grid
        self.generation += 1
    
    def display_console(self):
        """Menampilkan grid di console"""
        os.system('cls' if os.name == 'nt' else 'clear')  # Bersihkan layar
        print(f"=== Game of Life - Generasi {self.generation} ===")
        print("=" * (self.cols * 2 + 10))
        
        for row in range(self.rows):
            line = ""
            for col in range(self.cols):
                if self.grid[row][col] == 1:
                    line += "■ "  # Sel hidup
                else:
                    line += "□ "  # Sel mati
            print(line)
        print("=" * (self.cols * 2 + 10))
    
    def is_empty(self):
        """Memeriksa apakah semua sel mati"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:
                    return False
        return True
    
    def get_population(self):
        """Menghitung jumlah sel hidup"""
        population = 0
        for row in range(self.rows):
            for col in range(self.cols):
                population += self.grid[row][col]
        return population
    
    def run_console(self, max_generations=100, delay=0.5):
        """
        Menjalankan simulasi Game of Life di console
        Args:
            max_generations: maksimum generasi yang akan dijalankan
            delay: jeda antar generasi (detik)
        """
        generation = 0
        while generation < max_generations and not self.is_empty():
            self.display_console()
            self.next_generation()
            generation += 1
            time.sleep(delay)
        
        self.display_console()
        if self.is_empty():
            print("\nSemua organisme telah punah!")
        else:
            print(f"\nSimulasi selesai setelah {generation} generasi")


# ==================== PATTERN SETUP ====================
def setup_pattern(game, pattern_name):
    """
    Mengatur pola awal berdasarkan contoh dalam dokumen
    """
    # Pola 1: Konfigurasi sederhana (dari dokumen)
    if pattern_name == "simple":
        # Bentuk L kecil
        game.set_cell(10, 10, 1)
        game.set_cell(10, 11, 1)
        game.set_cell(11, 10, 1)
        game.set_cell(11, 11, 1)
        game.set_cell(12, 12, 1)
    
    # Pola 2: Blok stabil (dari dokumen)
    elif pattern_name == "block":
        # Blok 2x2 - stabil
        game.set_cell(10, 10, 1)
        game.set_cell(10, 11, 1)
        game.set_cell(11, 10, 1)
        game.set_cell(11, 11, 1)
    
    # Pola 3: Two-phase oscillator (dari dokumen)
    elif pattern_name == "oscillator":
        # Blinker (periode 2)
        game.set_cell(10, 10, 1)
        game.set_cell(10, 11, 1)
        game.set_cell(10, 12, 1)
    
    # Pola 4: Glider (bergerak)
    elif pattern_name == "glider":
        game.set_cell(5, 5, 1)
        game.set_cell(5, 6, 1)
        game.set_cell(6, 5, 1)
        game.set_cell(6, 6, 1)
        game.set_cell(7, 7, 1)
    
    # Pola 5: Contoh dari dokumen
    elif pattern_name == "document_example":
        # Contoh konfigurasi awal dari dokumen
        game.set_cell(10, 10, 1)
        game.set_cell(10, 11, 1)
        game.set_cell(11, 10, 1)
        game.set_cell(11, 11, 1)
        game.set_cell(12, 10, 1)
    
    # Pola 6: Acak
    elif pattern_name == "random":
        for row in range(game.rows):
            for col in range(game.cols):
                if random.random() < 0.3:  # 30% kemungkinan hidup
                    game.set_cell(row, col, 1)
    
    return game


# ==================== CONSOLE VERSION ====================
def run_console_version():
    """Menjalankan versi console"""
    print("=" * 50)
    print("      SELAMAT DATANG DI GAME OF LIFE (CONSOLE)")
    print("=" * 50)
    print("\nGame of Life adalah cellular automaton yang diciptakan")
    print("oleh matematikawan John Horton Conway pada tahun 1970.")
    print("\nAturan Permainan:")
    print("1. Sel hidup dengan 2-3 tetangga hidup tetap hidup")
    print("2. Sel hidup dengan < 2 tetangga mati (terisolasi)")
    print("3. Sel hidup dengan > 3 tetangga mati (kelebihan populasi)")
    print("4. Sel mati dengan tepat 3 tetangga menjadi hidup")
    print("=" * 50)
    
    # Ukuran grid
    rows, cols = 20, 40
    
    # Pilihan pola
    print("\nPilih pola awal:")
    print("1. Simple pattern (pola sederhana)")
    print("2. Block (blok stabil 2x2)")
    print("3. Oscillator (Blinker - periode 2)")
    print("4. Glider (bergerak)")
    print("5. Document example (contoh dari dokumen)")
    print("6. Random pattern")
    
    choice = input("\nMasukkan pilihan (1-6): ").strip()
    
    # Buat instance Game of Life
    game = GameOfLife(rows, cols)
    
    # Setup pola berdasarkan pilihan
    patterns = {
        '1': 'simple',
        '2': 'block',
        '3': 'oscillator',
        '4': 'glider',
        '5': 'document_example',
        '6': 'random'
    }
    
    if choice in patterns:
        game = setup_pattern(game, patterns[choice])
    else:
        print("Pilihan tidak valid, menggunakan pola default (simple)")
        game = setup_pattern(game, 'simple')
    
    # Jalankan simulasi
    print("\nMemulai simulasi...")
    print("Tekan Ctrl+C untuk menghentikan simulasi")
    input("Tekan Enter untuk melanjutkan...")
    
    try:
        game.run_console(max_generations=100, delay=0.2)
    except KeyboardInterrupt:
        print("\n\nSimulasi dihentikan oleh pengguna.")


# ==================== GUI VERSION ====================
class GameOfLifeGUI:
    """GUI untuk Game of Life"""
    
    def __init__(self, rows=30, cols=50, cell_size=15):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.game = GameOfLife(rows, cols)
        self.running = False
        self.speed = 200  # milliseconds
        
        # Buat window
        self.root = tk.Tk()
        self.root.title("Conway's Game of Life")
        
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame untuk canvas
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(padx=5, pady=5)
        
        # Canvas untuk grid
        self.canvas = tk.Canvas(
            canvas_frame,
            width=cols * cell_size,
            height=rows * cell_size,
            bg='white',
            highlightthickness=1,
            highlightbackground='gray'
        )
        self.canvas.pack()
        
        # Bind click event
        self.canvas.bind('<Button-1>', self.toggle_cell)
        self.canvas.bind('<B1-Motion>', self.drag_cell)
        
        # Frame untuk kontrol
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        # Tombol kontrol
        self.start_btn = ttk.Button(
            control_frame,
            text="▶ Start",
            command=self.start_simulation,
            width=12
        )
        self.start_btn.pack(side=tk.LEFT, padx=3)
        
        self.stop_btn = ttk.Button(
            control_frame,
            text="⏸ Stop",
            command=self.stop_simulation,
            width=12,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=3)
        
        self.clear_btn = ttk.Button(
            control_frame,
            text="🗑 Clear",
            command=self.clear_grid,
            width=12
        )
        self.clear_btn.pack(side=tk.LEFT, padx=3)
        
        self.random_btn = ttk.Button(
            control_frame,
            text="🎲 Random",
            command=self.random_grid,
            width=12
        )
        self.random_btn.pack(side=tk.LEFT, padx=3)
        
        # Frame untuk pola preset
        preset_frame = ttk.Frame(main_frame)
        preset_frame.pack(pady=5)
        
        ttk.Label(preset_frame, text="Pola Preset:").pack(side=tk.LEFT, padx=5)
        
        patterns = [
            ("Simple", "simple"),
            ("Block", "block"),
            ("Oscillator", "oscillator"),
            ("Glider", "glider"),
            ("Document", "document_example")
        ]
        
        for text, pattern in patterns:
            btn = ttk.Button(
                preset_frame,
                text=text,
                command=lambda p=pattern: self.load_pattern(p),
                width=8
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Frame untuk informasi
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=5)
        
        self.generation_label = ttk.Label(
            info_frame,
            text="Generasi: 0",
            font=('Arial', 10, 'bold')
        )
        self.generation_label.pack(side=tk.LEFT, padx=15)
        
        self.population_label = ttk.Label(
            info_frame,
            text="Populasi: 0",
            font=('Arial', 10, 'bold')
        )
        self.population_label.pack(side=tk.LEFT, padx=15)
        
        # Speed control
        speed_frame = ttk.Frame(main_frame)
        speed_frame.pack(pady=5)
        
        ttk.Label(speed_frame, text="Kecepatan:").pack(side=tk.LEFT)
        self.speed_scale = ttk.Scale(
            speed_frame,
            from_=50,
            to=1000,
            orient=tk.HORIZONTAL,
            length=200,
            command=self.change_speed
        )
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side=tk.LEFT, padx=10)
        
        # Status bar
        self.status_label = ttk.Label(
            main_frame,
            text="Klik pada grid untuk menempatkan/menghapus organisme",
            foreground='gray'
        )
        self.status_label.pack(pady=5)
        
        # Draw initial grid
        self.draw_grid()
        
    def draw_grid(self):
        """Menggambar grid"""
        self.canvas.delete("all")
        
        # Draw cells
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if self.game.get_cell(row, col) == 1:
                    color = '#2c3e50'  # Dark blue-gray for alive
                else:
                    color = '#ecf0f1'  # Light gray for dead
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='#bdc3c7',
                    width=1,
                    tags=f"cell_{row}_{col}"
                )
        
        # Update labels
        self.generation_label.config(text=f"Generasi: {self.game.generation}")
        self.population_label.config(text=f"Populasi: {self.game.get_population()}")
        
    def toggle_cell(self, event):
        """Toggle cell ketika diklik"""
        if not self.running:
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            
            if 0 <= row < self.rows and 0 <= col < self.cols:
                current = self.game.get_cell(row, col)
                self.game.set_cell(row, col, 1 - current)
                self.draw_grid()
                self.status_label.config(text=f"Mengubah sel ({row}, {col})")
    
    def drag_cell(self, event):
        """Mengubah cell saat drag mouse"""
        if not self.running:
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            
            if 0 <= row < self.rows and 0 <= col < self.cols:
                # Set cell menjadi hidup saat drag
                if self.game.get_cell(row, col) == 0:
                    self.game.set_cell(row, col, 1)
                    self.draw_grid()
    
    def load_pattern(self, pattern_name):
        """Memuat pola preset"""
        if not self.running:
            self.game = GameOfLife(self.rows, self.cols)
            self.game = setup_pattern(self.game, pattern_name)
            self.draw_grid()
            self.status_label.config(text=f"Memuat pola: {pattern_name}")
    
    def start_simulation(self):
        """Memulai simulasi"""
        if self.game.get_population() > 0:
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.clear_btn.config(state=tk.DISABLED)
            self.random_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Simulasi berjalan...")
            self.run_simulation()
    
    def stop_simulation(self):
        """Menghentikan simulasi"""
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.NORMAL)
        self.random_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Simulasi dihentikan")
    
    def clear_grid(self):
        """Membersihkan grid"""
        if not self.running:
            self.game = GameOfLife(self.rows, self.cols)
            self.draw_grid()
            self.status_label.config(text="Grid dibersihkan")
    
    def random_grid(self):
        """Membuat grid acak"""
        if not self.running:
            self.game = GameOfLife(self.rows, self.cols)
            self.game = setup_pattern(self.game, "random")
            self.draw_grid()
            self.status_label.config(text="Membuat pola acak")
    
    def change_speed(self, value):
        """Mengubah kecepatan simulasi"""
        self.speed = int(float(value))
    
    def run_simulation(self):
        """Menjalankan satu langkah simulasi"""
        if self.running:
            if self.game.get_population() == 0:
                self.stop_simulation()
                self.status_label.config(text="Semua organisme telah punah!")
                return
            
            self.game.next_generation()
            self.draw_grid()
            
            # Jadwalkan langkah berikutnya
            self.root.after(self.speed, self.run_simulation)
    
    def run(self):
        """Menjalankan GUI"""
        self.root.mainloop()


# ==================== MAIN PROGRAM ====================
def main():
    """Fungsi utama untuk menjalankan program"""
    print("=" * 60)
    print("               CONWAY'S GAME OF LIFE")
    print("=" * 60)
    print("\nPilih mode tampilan:")
    print("1. Console Mode (teks sederhana)")
    print("2. GUI Mode (antarmuka grafis)")
    print("3. Keluar")
    
    choice = input("\nMasukkan pilihan (1-3): ").strip()
    
    if choice == '1':
        run_console_version()
    elif choice == '2':
        print("\nMemulai GUI Mode...")
        print("Pastikan Anda memiliki tkinter (biasanya sudah terinstall dengan Python)")
        print("Klik pada grid untuk menempatkan organisme")
        print("Tekan Start untuk memulai simulasi\n")
        try:
            gui = GameOfLifeGUI(rows=30, cols=60, cell_size=15)
            gui.run()
        except Exception as e:
            print(f"Error saat menjalankan GUI: {e}")
            print("\nMenggunakan console mode sebagai alternatif...")
            run_console_version()
    else:
        print("\nTerima kasih telah menggunakan program Game of Life!")
        return


if __name__ == "__main__":
    main()