# ============================================================
#  Big Integer ADT - Tugas Praktikum Linked List
#  Soal 1a : Implementasi menggunakan Singly Linked List
#  Soal 1b : Implementasi menggunakan Python List
#  Soal 2  : Tambahan Assignment Combo Operators
# ============================================================


# ============================================================
#  SOAL 1a — BigInteger menggunakan SINGLY LINKED LIST
# ============================================================

class _Node:
    """Node untuk singly linked list."""
    def __init__(self, digit):
        self.digit = digit   # satu digit (0–9)
        self.next  = None


class BigIntegerLL:
    """
    Big Integer ADT berbasis Singly Linked List.
    Setiap node menyimpan SATU digit.
    Digit disimpan dari LEAST-significant ke MOST-significant
    (sama seperti diagram di soal).

    Contoh  45839  →  head → 9 → 8 → 3 → 5 → 4 → None
    """

    # ----------------------------------------------------------
    # Konstruktor
    # ----------------------------------------------------------
    def __init__(self, initValue="0"):
        self._head  = None
        self._negative = False
        self._build(str(initValue).strip())

    def _build(self, s):
        """Bangun linked list dari string angka."""
        self._head = None
        if s.startswith('-'):
            self._negative = True
            s = s[1:]
        else:
            self._negative = False

        # Hilangkan leading zeros
        s = s.lstrip('0') or '0'

        # Masukkan digit dari kiri ke kanan → digit terkiri = paling signifikan
        # Karena kita simpan dari least-significant, kita insert di DEPAN
        for ch in s:
            node = _Node(int(ch))
            node.next = self._head
            self._head = node

    def _to_int(self):
        """Konversi linked list ke int Python (untuk operasi aritmatika)."""
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        # digits sekarang least-significant first → balik
        value = int(''.join(reversed(digits)))
        return -value if self._negative else value

    # ----------------------------------------------------------
    # toString
    # ----------------------------------------------------------
    def toString(self):
        """Kembalikan representasi string dari big integer."""
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        result = ''.join(reversed(digits))
        return ('-' + result) if self._negative else result

    def __repr__(self):
        return f"BigIntegerLL('{self.toString()}')"

    def __str__(self):
        return self.toString()

    # ----------------------------------------------------------
    # comparable
    # ----------------------------------------------------------
    def comparable(self, other):
        """
        Bandingkan self dengan other.
        Return: -1  jika self < other
                 0  jika self == other
                 1  jika self > other
        """
        a = self._to_int()
        b = other._to_int()
        if a < b:  return -1
        if a > b:  return  1
        return 0

    def __lt__(self, other): return self.comparable(other) == -1
    def __le__(self, other): return self.comparable(other) <= 0
    def __gt__(self, other): return self.comparable(other) == 1
    def __ge__(self, other): return self.comparable(other) >= 0
    def __eq__(self, other): return self.comparable(other) == 0
    def __ne__(self, other): return self.comparable(other) != 0

    # ----------------------------------------------------------
    # arithmetic
    # ----------------------------------------------------------
    def arithmetic(self, rhsInt, op):
        """
        Kembalikan BigIntegerLL baru hasil operasi aritmatika.
        op: '+', '-', '*', '//', '%', '**'
        """
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '+':  lambda x, y: x + y,
            '-':  lambda x, y: x - y,
            '*':  lambda x, y: x * y,
            '//': lambda x, y: x // y,
            '%':  lambda x, y: x % y,
            '**': lambda x, y: x ** y,
        }
        if op not in ops:
            raise ValueError(f"Operator aritmatika tidak dikenal: '{op}'")
        result = ops[op](a, b)
        return BigIntegerLL(str(result))

    def __add__(self, other): return self.arithmetic(other, '+')
    def __sub__(self, other): return self.arithmetic(other, '-')
    def __mul__(self, other): return self.arithmetic(other, '*')
    def __floordiv__(self, other): return self.arithmetic(other, '//')
    def __mod__(self, other): return self.arithmetic(other, '%')
    def __pow__(self, other): return self.arithmetic(other, '**')

    # ----------------------------------------------------------
    # bitwise-ops
    # ----------------------------------------------------------
    def bitwise_ops(self, rhsInt, op):
        """
        Kembalikan BigIntegerLL baru hasil operasi bitwise.
        op: '|', '&', '^', '<<', '>>'
        """
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '|':  lambda x, y: x | y,
            '&':  lambda x, y: x & y,
            '^':  lambda x, y: x ^ y,
            '<<': lambda x, y: x << y,
            '>>': lambda x, y: x >> y,
        }
        if op not in ops:
            raise ValueError(f"Operator bitwise tidak dikenal: '{op}'")
        result = ops[op](a, b)
        return BigIntegerLL(str(result))

    def __or__(self, other):  return self.bitwise_ops(other, '|')
    def __and__(self, other): return self.bitwise_ops(other, '&')
    def __xor__(self, other): return self.bitwise_ops(other, '^')
    def __lshift__(self, other): return self.bitwise_ops(other, '<<')
    def __rshift__(self, other): return self.bitwise_ops(other, '>>')

    # ----------------------------------------------------------
    # SOAL 2 — Assignment Combo Operators
    # ----------------------------------------------------------
    def __iadd__(self, other):
        res = self.arithmetic(other, '+');  self._build(res.toString()); return self
    def __isub__(self, other):
        res = self.arithmetic(other, '-');  self._build(res.toString()); return self
    def __imul__(self, other):
        res = self.arithmetic(other, '*');  self._build(res.toString()); return self
    def __ifloordiv__(self, other):
        res = self.arithmetic(other, '//'); self._build(res.toString()); return self
    def __imod__(self, other):
        res = self.arithmetic(other, '%');  self._build(res.toString()); return self
    def __ipow__(self, other):
        res = self.arithmetic(other, '**'); self._build(res.toString()); return self
    def __ilshift__(self, other):
        res = self.bitwise_ops(other, '<<'); self._build(res.toString()); return self
    def __irshift__(self, other):
        res = self.bitwise_ops(other, '>>'); self._build(res.toString()); return self
    def __ior__(self, other):
        res = self.bitwise_ops(other, '|'); self._build(res.toString()); return self
    def __iand__(self, other):
        res = self.bitwise_ops(other, '&'); self._build(res.toString()); return self
    def __ixor__(self, other):
        res = self.bitwise_ops(other, '^'); self._build(res.toString()); return self


# ============================================================
#  SOAL 1b — BigInteger menggunakan PYTHON LIST
# ============================================================

class BigIntegerList:
    """
    Big Integer ADT berbasis Python list.
    Digit disimpan dari LEAST-significant ke MOST-significant.

    Contoh  45839  →  [9, 8, 3, 5, 4]
    """

    # ----------------------------------------------------------
    # Konstruktor
    # ----------------------------------------------------------
    def __init__(self, initValue="0"):
        self._digits   = []
        self._negative = False
        self._build(str(initValue).strip())

    def _build(self, s):
        if s.startswith('-'):
            self._negative = True
            s = s[1:]
        else:
            self._negative = False
        s = s.lstrip('0') or '0'
        # Simpan digit least-significant first
        self._digits = [int(ch) for ch in reversed(s)]

    def _to_int(self):
        value = int(''.join(str(d) for d in reversed(self._digits)))
        return -value if self._negative else value

    # ----------------------------------------------------------
    # toString
    # ----------------------------------------------------------
    def toString(self):
        result = ''.join(str(d) for d in reversed(self._digits))
        return ('-' + result) if self._negative else result

    def __repr__(self):
        return f"BigIntegerList('{self.toString()}')"

    def __str__(self):
        return self.toString()

    # ----------------------------------------------------------
    # comparable
    # ----------------------------------------------------------
    def comparable(self, other):
        a = self._to_int()
        b = other._to_int()
        if a < b:  return -1
        if a > b:  return  1
        return 0

    def __lt__(self, other): return self.comparable(other) == -1
    def __le__(self, other): return self.comparable(other) <= 0
    def __gt__(self, other): return self.comparable(other) == 1
    def __ge__(self, other): return self.comparable(other) >= 0
    def __eq__(self, other): return self.comparable(other) == 0
    def __ne__(self, other): return self.comparable(other) != 0

    # ----------------------------------------------------------
    # arithmetic
    # ----------------------------------------------------------
    def arithmetic(self, rhsInt, op):
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '+':  lambda x, y: x + y,
            '-':  lambda x, y: x - y,
            '*':  lambda x, y: x * y,
            '//': lambda x, y: x // y,
            '%':  lambda x, y: x % y,
            '**': lambda x, y: x ** y,
        }
        if op not in ops:
            raise ValueError(f"Operator aritmatika tidak dikenal: '{op}'")
        return BigIntegerList(str(ops[op](a, b)))

    def __add__(self, other): return self.arithmetic(other, '+')
    def __sub__(self, other): return self.arithmetic(other, '-')
    def __mul__(self, other): return self.arithmetic(other, '*')
    def __floordiv__(self, other): return self.arithmetic(other, '//')
    def __mod__(self, other): return self.arithmetic(other, '%')
    def __pow__(self, other): return self.arithmetic(other, '**')

    # ----------------------------------------------------------
    # bitwise-ops
    # ----------------------------------------------------------
    def bitwise_ops(self, rhsInt, op):
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '|':  lambda x, y: x | y,
            '&':  lambda x, y: x & y,
            '^':  lambda x, y: x ^ y,
            '<<': lambda x, y: x << y,
            '>>': lambda x, y: x >> y,
        }
        if op not in ops:
            raise ValueError(f"Operator bitwise tidak dikenal: '{op}'")
        return BigIntegerList(str(ops[op](a, b)))

    def __or__(self, other):  return self.bitwise_ops(other, '|')
    def __and__(self, other): return self.bitwise_ops(other, '&')
    def __xor__(self, other): return self.bitwise_ops(other, '^')
    def __lshift__(self, other): return self.bitwise_ops(other, '<<')
    def __rshift__(self, other): return self.bitwise_ops(other, '>>')

    # ----------------------------------------------------------
    # SOAL 2 — Assignment Combo Operators
    # ----------------------------------------------------------
    def __iadd__(self, other):
        self._build(self.arithmetic(other, '+').toString()); return self
    def __isub__(self, other):
        self._build(self.arithmetic(other, '-').toString()); return self
    def __imul__(self, other):
        self._build(self.arithmetic(other, '*').toString()); return self
    def __ifloordiv__(self, other):
        self._build(self.arithmetic(other, '//').toString()); return self
    def __imod__(self, other):
        self._build(self.arithmetic(other, '%').toString()); return self
    def __ipow__(self, other):
        self._build(self.arithmetic(other, '**').toString()); return self
    def __ilshift__(self, other):
        self._build(self.bitwise_ops(other, '<<').toString()); return self
    def __irshift__(self, other):
        self._build(self.bitwise_ops(other, '>>').toString()); return self
    def __ior__(self, other):
        self._build(self.bitwise_ops(other, '|').toString()); return self
    def __iand__(self, other):
        self._build(self.bitwise_ops(other, '&').toString()); return self
    def __ixor__(self, other):
        self._build(self.bitwise_ops(other, '^').toString()); return self


# ============================================================
#  DEMO / TESTING
# ============================================================

def demo(cls, label):
    print("=" * 60)
    print(f"  {label}")
    print("=" * 60)

    a = cls("45839")
    b = cls("123")

    print(f"\n[toString]")
    print(f"  a = {a.toString()}")
    print(f"  b = {b.toString()}")

    print(f"\n[comparable]  a.comparable(b) = {a.comparable(b)}")
    print(f"  a < b  : {a < b}")
    print(f"  a > b  : {a > b}")
    print(f"  a == b : {a == b}")
    print(f"  a != b : {a != b}")

    print(f"\n[arithmetic]")
    print(f"  a + b  = {a.arithmetic(b, '+')}")
    print(f"  a - b  = {a.arithmetic(b, '-')}")
    print(f"  a * b  = {a.arithmetic(b, '*')}")
    print(f"  a // b = {a.arithmetic(b, '//')}")
    print(f"  a % b  = {a.arithmetic(b, '%')}")
    print(f"  b ** cls('3') = {b.arithmetic(cls('3'), '**')}")

    print(f"\n[bitwise-ops]")
    x = cls("255")
    y = cls("170")
    print(f"  255 | 170  = {x.bitwise_ops(y, '|')}")
    print(f"  255 & 170  = {x.bitwise_ops(y, '&')}")
    print(f"  255 ^ 170  = {x.bitwise_ops(y, '^')}")
    print(f"  255 << 2   = {x.bitwise_ops(cls('2'), '<<')}")
    print(f"  255 >> 2   = {x.bitwise_ops(cls('2'), '>>')}")

    print(f"\n[Soal 2 — Assignment Combo Operators]")
    c = cls("1000")
    d = cls("7")
    print(f"  c = {c},  d = {d}")
    c += d;  print(f"  c += d  → {c}")
    c -= d;  print(f"  c -= d  → {c}")
    c *= d;  print(f"  c *= d  → {c}")
    c //= d; print(f"  c //= d → {c}")
    c %= d;  print(f"  c %= d  → {c}")

    e = cls("2")
    f = cls("10")
    e **= f; print(f"  2 **= 10 → {e}")

    g = cls("255")
    h = cls("2")
    g <<= h; print(f"  255 <<= 2 → {g}")
    g >>= h; print(f"  {g} >>= 2 → ", end=""); g >>= h; print(g)

    p = cls("170")
    q = cls("255")
    p |= q;  print(f"  170 |= 255  → {p}")
    p &= q;  print(f"  {p} &= 255  → ", end=""); p &= q; print(p)
    p ^= q;  print(f"  {p} ^= 255  → ", end=""); p ^= q; print(p)

    print()


if __name__ == "__main__":
    demo(BigIntegerLL,   "Soal 1a — BigInteger dengan Singly Linked List")
    demo(BigIntegerList, "Soal 1b — BigInteger dengan Python List")