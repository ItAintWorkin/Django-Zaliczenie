import math


class Bitarray:

    def __init__(self):
        self.__bytearray = bytearray([0])
        self.__length = 0

    def __len__(self) -> int:
        return self.__length

    def __str__(self):
        s = "{0:b}".format(self.__bytearray[0])
        for i in range(1, len(self.__bytearray)):
            s += " {0:08b}".format(self.__bytearray[i])
        return s

    def __getitem__(self, item):
        ib = len(self.__bytearray) * 8 - len(self) + item

        B = ib // 8
        b = ib % 8

        return (self.__bytearray[B] >> (7-b)) & 1

    def __setitem__(self, item, value):
        ib = len(self.__bytearray) * 8 - len(self) + item
        B = ib // 8
        b = ib % 8

        self.__bytearray[B] &= 0xff ^ (1 << (7-b))
        self.__bytearray[B] |= value << (7-b)
        return

    @classmethod
    def from_boolean_matrix(cls, matrix: list):
        bitarray = cls()
        for y in range(len(matrix)):
            for x in range(len(matrix)):
                value = matrix[x][y]
                if value is None or value==0:
                    value = 0
                else:
                    value = 1
                bitarray.append(bytearray([value]),1)
        return bitarray

    def to_boolean_matrix(self):
        w = math.sqrt(len(self))
        if int(w) != w:
            raise ValueError("Length of bitarray is not a square")
        w = int(w)
        matrix = []
        for x in range(w):
            row = []
            for y in range(w):
                row.append(self[y*w+x])
            matrix.append(row)
        return matrix


    def get_bytearray(self):
        return self.__bytearray

    def append(self, data: bytearray, length: int):
        self.__shift_left(length)
        for i in range(length // 8):
            self.__bytearray[-(length // 8 - i)] = data[i]
        if length % 8 != 0:
            self.__bytearray[-length // 8] |= data[0]

    def pad_bits(self):
        self.__shift_left((8 - (self.__length % 8)) % 8)

    def pad_bytes(self, total_bytes):
        pad_codewords = [bytearray([0b11101100]), bytearray([0b00010001])]
        p = 0
        if self.__length % 8 != 0:
            self.pad_bits()
        for i in range(self.__length // 8, total_bytes):
            self.append(pad_codewords[p % 2], 8)
            p += 1

    def __shift_left(self, offset: int):
        while len(self.__bytearray) * 8 < self.__length + offset:
            self.__bytearray.insert(0, 0)
        for i in range(len(self)):
            self[i-offset] = self[i]
            self[i] = 0
        self.__length += offset
        return self.__bytearray
