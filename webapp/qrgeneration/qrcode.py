class QRCode:

    def __init__(self, data: str):
        if len(data) > 19:
            raise NotImplementedError("QR codes with text up to 19 is only supported for now")

        self.__version = 1  # for now let's just use the smallest  size TODO: implement other versions
        self.__mask = 1
        self.__error_correction = "L"
        self.data = data
        self.matrix = [[None for _ in range(self.get_width())] for _ in range(self.get_width())]

        self.__insert_function_patterns()

        codewords = self.__Codewords()
        codewords.append(bytearray([4]), 4)  # 0b0100 represents byte mode TODO: implement other modes
        codewords.append(bytearray([len(data)]),
                         8)  #  Table 3 - For byte mode and versions 1-9 the bit count is 8 TODO: implement other modes and versions
        codewords.append(bytearray(data.encode(encoding="ascii")), len(data) * 8)
        codewords.pad_bytes(26 - self.__get_number_of_error_correction_codewords())
        codewords.append(self.__get_error_correction_codewords(codewords, 26),
                         self.__get_number_of_error_correction_codewords() * 8)

        self.__insert_format_information()
        self.__populate_matrix(codewords)
        self.__apply_mask()

    def __insert_function_patterns(self):
        self.__insert_finder_patterns()
        self.__insert_separators()
        self.__insert_timing_patterns()
        self.__insert_alignment_patterns()

    def __insert_finder_patterns(self):
        for pos in [(0, 0), (0, self.get_width() - 7), (self.get_width() - 7, 0)]:
            for x in range(7):
                for y in range(7):
                    if (1 <= x < 6 and 1 <= y < 6) and (x < 2 or x >= 5 or y < 2 or y >= 5):
                        self.matrix[pos[0] + x][pos[1] + y] = 0
                    else:
                        self.matrix[pos[0] + x][pos[1] + y] = 1

    def __insert_separators(self):
        for i in range(8):
            self.matrix[i][7] = 0
            self.matrix[7][i] = 0

            self.matrix[i][self.get_width() - 7 - 1] = 0
            self.matrix[7][self.get_width() - i - 1] = 0

            self.matrix[self.get_width() - i - 1][7] = 0
            self.matrix[self.get_width() - 7 - 1][i] = 0

    def __insert_timing_patterns(self):
        for i in range(8, self.get_width() - 7):
            self.matrix[6][i] = (i + 1) % 2
            self.matrix[i][6] = (i + 1) % 2

    def __insert_alignment_patterns(self):
        if self.__version == 1:
            return
        raise NotImplementedError("Alignment patterns not implemented for QR versions bigger than 1")

    def __insert_format_information(self):
        format_information = []
        match self.__error_correction:
            case 'l' | 'L':
                format_information.append(0)
                format_information.append(1)
            case 'm' | 'M':
                format_information.append(0)
                format_information.append(0)
            case 'q' | 'Q':
                format_information.append(1)
                format_information.append(1)
            case 'h' | 'H':
                format_information.append(1)
                format_information.append(0)
        format_information.append((self.__mask >> 2) & 1)
        format_information.append((self.__mask >> 1) & 1)
        format_information.append((self.__mask) & 1)

        GCH = format_information.copy() + [0] * 10
        G = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1]
        for p in range(5):
            if GCH[p] == 1:
                for i in range(11):
                    GCH[p + i] ^= G[i]
        format_information += GCH[5:]

        # XOR mask
        for i in [0, 2, 4, 10, 13]:
            format_information[i] = (format_information[i] + 1) % 2

        format_information.reverse()
        for i in range(6):
            self.matrix[8][i] = format_information[i]
            self.matrix[self.get_width() - 1 - i][8] = format_information[i]

        self.matrix[8][7] = format_information[6]
        self.matrix[8][8] = format_information[7]
        self.matrix[7][8] = format_information[8]

        self.matrix[self.get_width() - 1 - 6][8] = format_information[6]
        self.matrix[self.get_width() - 1 - 7][8] = format_information[7]
        self.matrix[8][self.get_width() - 1 - 6] = format_information[8]

        for i in range(9, 15):
            self.matrix[14 - i][8] = format_information[i]
            self.matrix[8][self.get_width() - 1 - 14 + i] = format_information[i]

        self.matrix[8][self.get_width() - 1 - 7] = 1

    def __populate_matrix(self, codewords: self.__Codewords):
        ba = codewords.get_bytearray()
        coords = [self.get_width() - 1, self.get_width() - 1]

        for b in range((8 - (len(codewords) % 8)) % 8, 8):
            value = (ba[0] << b & 128) >> 7
            coords = self.__put_module(coords, value)
            continue

        for B in range(1, len(ba)):
            for b in range(8):
                value = (ba[B] << b & 128) >> 7
                coords = self.__put_module(coords, value)
                if coords is None:
                    raise ValueError("Could not find a place to put a module. " + str(len(ba) - B) + "B " + str(8-b) + "b remaining." )

    def __put_module(self, coords: list, value: int):
        """
        Tries to put module in specified coordinates.
        :param coords: coords at which to try to place value
        :param value: value to put
        :return: coordinate at which the function succeeded or None if failed
        """
        if not isinstance(coords, list) and len(coords) != 2:
            raise ValueError("coords must be a list of length two")

        while self.matrix[coords[0]][coords[1]] is not None:
            # 1 if up, -1 if down, and 0 if left
            direction = 1 - coords[0] % 2 if coords[0] < 6 else coords[0] % 2
            if direction != 0 and ((coords[0] - self.get_width() - 1) // 2) % 2 != 0:
                direction *= -1

            coords[1] -= direction
            coords[0] += -1 if direction == 0 else 1
            if coords[1] < 0:
                coords[1] = 0
                coords[0] -= 2
            elif coords[1] >= self.get_width():
                coords[1] = self.get_width() - 1
                coords[0] -= 2
            if coords[0] < 0:
                return None

        self.matrix[coords[0]][coords[1]] = value

        return coords

    def __str__(self):
        out = ""
        for y in range(-4, self.get_width() + 4):
            for x in range(-4, self.get_width() + 4):
                if x < 0 or x >= self.get_width() or y < 0 or y >= self.get_width():
                    out += "\x1b[107m \x1b[0m"
                    continue
                val = self.matrix[x][y]
                if val is None:
                    out += "?"  # this is purely for debugging purposes
                elif val == 0:
                    out += "\x1b[107m \x1b[0m"
                else:
                    out += "\x1b[40m \x1b[0m"

            out += '\n'

        return out

    def __get_number_of_error_correction_codewords(self):
        if self.__version == 1:
            match self.__error_correction:
                case 'l' | 'L':
                    return 7
                case 'm' | 'M':
                    return 10
                case 'q' | 'Q':
                    return 13
                case 'h' | 'H':
                    return 17
        else:
            raise NotImplementedError("QR code version 1 is only supported")

    def get_width(self):
        return 17 + 4 * self.__version

    def __is_in_functional_patterns(self, x:int, y:int):
        """
        Checks if module at (x,y) is a part of functional_patterns. The left upper corner has coordinates of (0,0)
        """
        if (x < 9 and y < 9):  # left square
            return True
        if (x > self.get_width() - 9 and y < 9):  # right square
            return True
        if (x < 9 and y > self.get_width() - 9):  # bottom square
            return True
        if x == 6 or y == 6:  # timing strips
            return True
        return False

    def __apply_mask(self):
        for i in range(self.get_width()):
            for j in range(self.get_width()):
                if self.__is_in_functional_patterns(j, i):
                    continue
                if self.__mask_condition(i, j):
                    if self.matrix[j][i] is None:
                        continue
                    self.matrix[j][i] += 1
                    self.matrix[j][i] %= 2

    def __mask_condition(self, i, j):
        match self.__mask:
            case 0:
                return (i + j) % 2 == 0
            case 1:
                return i % 2 == 0
            case 2:
                return j % 3 == 0
            case 3:
                return (i + j) % 3 == 0
            case 4:
                return ((i // 2) + (j // 3)) % 2 == 0
            case 5:
                return (i * j) % 2 + (i * j) % 3 == 0
            case 6:
                return ((i * j) % 2 + (i * j) % 3) % 2 == 0
            case 7:
                return ((i + j) % 2 + (i * j) % 3) % 2 == 0

    class __Codewords:

        def __init__(self):
            self.__bytearray = bytearray([0])
            self.__length = 0

        def __len__(self) -> int:
            return self.__length

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
            if offset == 0:
                return self.__bytearray
            orginal_length = len(self.__bytearray)
            offset_B = offset // 8  # + (1 if offset % 8 != 0 else 0) # offset in bytes rounded up
            while len(self.__bytearray) * 8 < self.__length + offset:
                self.__bytearray.insert(0, 0)

            for i in range(0, orginal_length):
                self.__bytearray[i] = (self.__bytearray[i + offset_B] << (offset % 8)) & 255
                if i + offset_B + 1 < orginal_length:
                    self.__bytearray[i] |= self.__bytearray[i + offset_B + 1] >> (8 - (offset % 8))
            for i in range(orginal_length, len(self.__bytearray)):
                self.__bytearray[i] = 0

            self.__length += offset
            return self.__bytearray

        def __str__(self):
            return self.__bytearray.hex()

    # https://dev.to/maxart2501/let-s-develop-a-qr-code-generator-part-iii-error-correction-1kbm
    def __get_error_correction_codewords(self, data_codewords: self.__Codewords, total_length):
        GF = 0b100011101

        exp = [0] * 256
        log = [0] * 256

        val = 1
        for ex in range(1, 256):
            val = ((val << 1) ^ GF) if val > 127 else val << 1
            log[val] = ex % 255
            exp[ex % 255] = val

        def mul(a, b):
            return 0 if a == 0 or b == 0 else exp[(log[a] + log[b]) % 255]

        def div(a, b):
            return exp[(log[a] + log[b] * 254) % 255]

        def poly_mul(F, G):
            H = [0] * (len(F) + len(G) - 1)
            for i in range(len(H)):
                for p1 in range(i + 1):
                    p2 = i - p1
                    if (0 <= p1 < len(F) and 0 <= p2 < len(G)):
                        H[i] ^= mul(F[p1], G[p2])
            return H

        def poly_rem(F, G):
            R = F.copy()
            remainder_length = len(F) - len(G) + 1
            for i in range(remainder_length):
                a = div(R[i], G[0])
                for j in range(len(G)):
                    R[i + j] ^= mul(a, G[j])

            return R[remainder_length:]

        def get_generator_poly(deg):
            G = [1]
            for i in range(deg):
                G = poly_mul(G, [1, exp[i]])
            return G

        degree = total_length - len(data_codewords.get_bytearray())
        message_poly = data_codewords.get_bytearray() + bytearray([0] * degree)
        return poly_rem(message_poly, get_generator_poly(degree))


print(QRCode("Hello World!"))
