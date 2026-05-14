# =============================================
# NODE STRUKTUR
# =============================================

class TagNode:
    """Node untuk linked list per tag"""
    def __init__(self, note):
        self.note = note        # referensi ke NoteNode
        self.next_in_tag = None # link ke note lain dalam tag yang sama

class NoteNode:
    """Node utama untuk setiap note"""
    def __init__(self, title, content, tags=[]):
        self.title = title
        self.content = content
        self.tags = tags            # list nama tag

        # Doubly linked - chronological order
        self.prev_chron = None
        self.next_chron = None

        # Doubly linked - alphabetical order
        self.prev_alpha = None
        self.next_alpha = None

        # Multi-linked per tag (dict: tag_name -> TagNode)
        self.tag_links = {}

        import datetime
        self.created_at = datetime.datetime.now()


# =============================================
# CIRCULAR BUFFER untuk Sync Status
# =============================================

class CircularBuffer:
    """Melacak perubahan terakhir (recent changes)"""
    def __init__(self, capacity=10):
        self.buffer = [None] * capacity
        self.capacity = capacity
        self.head = 0   # pointer tulis
        self.size = 0

    def add_change(self, change_info):
        self.buffer[self.head] = change_info
        self.head = (self.head + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def get_recent(self):
        result = []
        for i in range(self.size):
            idx = (self.head - 1 - i) % self.capacity
            result.append(self.buffer[idx])
        return result


# =============================================
# APLIKASI NOTE-TAKING
# =============================================

class NoteTakingApp:
    def __init__(self):
        # Doubly linked list - chronological (head = terlama)
        self.chron_head = None
        self.chron_tail = None

        # Doubly linked list - alphabetical (head = A)
        self.alpha_head = None
        self.alpha_tail = None

        # Multi-linked: dict tag -> head of tag chain
        self.tag_map = {}

        # Circular buffer untuk sync status
        self.sync_buffer = CircularBuffer(capacity=10)

        self.total_notes = 0

    # ------------------------------------------
    # TAMBAH NOTE
    # ------------------------------------------
    def add_note(self, title, content, tags=[]):
        note = NoteNode(title, content, tags)

        # 1. Insert ke chronological (tambah di akhir = terbaru)
        self._insert_chron(note)

        # 2. Insert ke alphabetical (sorted by title)
        self._insert_alpha(note)

        # 3. Insert ke setiap tag chain (multi-linked)
        for tag in tags:
            self._insert_tag(note, tag)

        # 4. Catat ke circular buffer
        self.sync_buffer.add_change({
            'action': 'ADD',
            'title': title,
            'tags': tags
        })

        self.total_notes += 1
        print(f"✅ Note '{title}' ditambahkan dengan tags: {tags}")

    def _insert_chron(self, note):
        """Insert di akhir (chronological = urutan waktu)"""
        if self.chron_tail is None:
            self.chron_head = self.chron_tail = note
        else:
            note.prev_chron = self.chron_tail
            self.chron_tail.next_chron = note
            self.chron_tail = note

    def _insert_alpha(self, note):
        """Insert sorted by title (alphabetical)"""
        if self.alpha_head is None:
            self.alpha_head = self.alpha_tail = note
            return
        cur = self.alpha_head
        while cur and cur.title.lower() < note.title.lower():
            cur = cur.next_alpha
        if cur is None:
            # Insert di akhir
            note.prev_alpha = self.alpha_tail
            self.alpha_tail.next_alpha = note
            self.alpha_tail = note
        else:
            # Insert sebelum cur
            note.next_alpha = cur
            note.prev_alpha = cur.prev_alpha
            if cur.prev_alpha:
                cur.prev_alpha.next_alpha = note
            else:
                self.alpha_head = note
            cur.prev_alpha = note

    def _insert_tag(self, note, tag):
        """Tambahkan note ke chain tag tertentu"""
        tag_node = TagNode(note)
        note.tag_links[tag] = tag_node
        if tag not in self.tag_map:
            self.tag_map[tag] = tag_node
        else:
            tag_node.next_in_tag = self.tag_map[tag]
            self.tag_map[tag] = tag_node

    # ------------------------------------------
    # TAMPILKAN
    # ------------------------------------------
    def show_chronological(self):
        print("\n📅 Chronological View (terlama → terbaru):")
        cur = self.chron_head
        i = 1
        while cur:
            print(f"  {i}. [{cur.created_at.strftime('%H:%M:%S')}] {cur.title} {cur.tags}")
            cur = cur.next_chron
            i += 1

    def show_alphabetical(self):
        print("\n🔤 Alphabetical View (A → Z):")
        cur = self.alpha_head
        i = 1
        while cur:
            print(f"  {i}. {cur.title} {cur.tags}")
            cur = cur.next_alpha
            i += 1

    def show_by_tag(self, tag):
        print(f"\n🏷️  Notes dengan tag '{tag}':")
        if tag not in self.tag_map:
            print("  (tidak ada)")
            return
        cur = self.tag_map[tag]
        i = 1
        while cur:
            print(f"  {i}. {cur.note.title}")
            cur = cur.next_in_tag
            i += 1

    def show_recent_changes(self):
        print("\n🔄 Recent Sync Changes:")
        changes = self.sync_buffer.get_recent()
        for i, c in enumerate(changes):
            print(f"  {i+1}. [{c['action']}] {c['title']} → tags: {c['tags']}")


# =============================================
# CONTOH PENGGUNAAN
# =============================================

app = NoteTakingApp()

app.add_note("Belajar Python",   "Materi OOP",        tags=["coding", "belajar"])
app.add_note("Resep Nasi Goreng","Bahan dan cara masak", tags=["masakan"])
app.add_note("Algoritma DLL",    "Doubly Linked List", tags=["coding", "strukdat"])
app.add_note("Agenda Meeting",   "Besok jam 10",       tags=["kerja", "belajar"])
app.add_note("Catatan Harian",   "Hari yang produktif",tags=["harian"])

app.show_chronological()
app.show_alphabetical()
app.show_by_tag("coding")
app.show_by_tag("belajar")
app.show_recent_changes()