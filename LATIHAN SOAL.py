from typing import List, Dict, Optional

# 1. Deduplikasi dengan mempertahankan urutan
def deduplicate(lst: List) -> List:
    """
    Menghapus duplikat dari list dengan mempertahankan urutan kemunculan pertama.
    """
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# 2. Intersection dua array
def intersection(list1: List, list2: List) -> List:
    """
    Mengembalikan elemen yang muncul di kedua list.
    """
    set1 = set(list1)
    set2 = set(list2)
    return list(set1 & set2)

# 3. Anagram check
def is_anagram(s1: str, s2: str) -> bool:
    """
    Memeriksa apakah dua string adalah anagram.
    """
    # Normalisasi: hapus spasi dan ubah ke huruf kecil
    s1 = s1.replace(" ", "").lower()
    s2 = s2.replace(" ", "").lower()
    
    from collections import Counter
    return Counter(s1) == Counter(s2)

# 4. First Recurring Character
def first_recurring_char(s: str) -> Optional[str]:
    """
    Menemukan karakter pertama yang muncul lebih dari sekali.
    Mengembalikan None jika tidak ada.
    """
    seen = set()
    for char in s:
        if char in seen:
            return char
        seen.add(char)
    return None

# 5. Simulasi Buku Telepon (Class-based dengan dataclass)
from dataclasses import dataclass
from typing import Dict

@dataclass
class Contact:
    name: str
    phone: str

class PhoneBook:
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}
    
    def add_contact(self, name: str, phone: str) -> None:
        """Menambah atau memperbarui kontak."""
        self.contacts[name] = Contact(name, phone)
        print(f"Kontak '{name}' berhasil ditambahkan/diperbarui.")
    
    def search_contact(self, name: str) -> Optional[Contact]:
        """Mencari kontak berdasarkan nama."""
        return self.contacts.get(name)
    
    def display_all(self) -> None:
        """Menampilkan semua kontak."""
        if not self.contacts:
            print("Buku telepon kosong.")
            return
        
        print("\nDaftar Kontak:")
        for name, contact in self.contacts.items():
            print(f"  {name}: {contact.phone}")
    
    def run_menu(self):
        """Menjalankan menu interaktif."""
        while True:
            print("\n=== BUKU TELEPON ===")
            print("1. Tambah kontak")
            print("2. Cari kontak")
            print("3. Tampilkan semua")
            print("4. Keluar")
            
            choice = input("Pilih menu (1-4): ").strip()
            
            if choice == "1":
                name = input("Nama: ").strip()
                phone = input("Nomor telepon: ").strip()
                self.add_contact(name, phone)
            
            elif choice == "2":
                name = input("Nama yang dicari: ").strip()
                contact = self.search_contact(name)
                if contact:
                    print(f"Nomor {contact.name}: {contact.phone}")
                else:
                    print(f"Kontak '{name}' tidak ditemukan.")
            
            elif choice == "3":
                self.display_all()
            
            elif choice == "4":
                print("Terima kasih telah menggunakan buku telepon!")
                break
            
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

# Contoh penggunaan
if __name__ == "__main__":
    # Test soal 1
    print("=== SOAL 1: Deduplikasi ===")
    data = [3, 1, 2, 1, 3, 4, 2, 5]
    print(f"Input: {data}")
    print(f"Hasil: {deduplicate(data)}")
    
    # Test soal 2
    print("\n=== SOAL 2: Intersection ===")
    a = [1, 2, 3, 4, 5]
    b = [3, 4, 5, 6, 7]
    print(f"List1: {a}")
    print(f"List2: {b}")
    print(f"Irisan: {intersection(a, b)}")
    
    # Test soal 3
    print("\n=== SOAL 3: Anagram Check ===")
    kata1 = "listen"
    kata2 = "silent"
    print(f"'{kata1}' dan '{kata2}': {is_anagram(kata1, kata2)}")
    
    kata3 = "hello"
    kata4 = "world"
    print(f"'{kata3}' dan '{kata4}': {is_anagram(kata3, kata4)}")
    
    # Test soal 4
    print("\n=== SOAL 4: First Recurring Character ===")
    text = "ABCA"
    print(f"String: '{text}'")
    print(f"Karakter pertama yang berulang: {first_recurring_char(text)}")
    
    text2 = "ABCD"
    print(f"String: '{text2}'")
    print(f"Karakter pertama yang berulang: {first_recurring_char(text2)}")
    
    # Test soal 5
    print("\n=== SOAL 5: Buku Telepon ===")
    phonebook = PhoneBook()
    phonebook.run_menu()