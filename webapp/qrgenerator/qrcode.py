from qrgenerator.tables_and_enums import *
from qrgenerator.bitarray import Bitarray

def get_minimal_version(mode: Mode, data: str, ecl: ErrorCorrectionLevel = ErrorCorrectionLevel.M):
    if mode != Mode.BYTE:
        raise NotImplementedError("can't get minimal version of modes different than byte(0b0100), got " + str(mode))
    for i in range(1, 7):
        if len(data) < TABLE_7_BYTE[i][ecl.value]:
            return i
    raise NotImplementedError(
        "qrcodes for version 7 and higher require Version Information (7.10) which is not implemented")

def update_matrix(qr: QRCode):

    qr["matrix"] = [[None for _ in range(qr.get_width())] for _ in range(qr.get_width())]

    __insert_function_patterns(qr)
    codewords = Bitarray()
    codewords.append(bytearray([qr["mode"].value]), 4)
    codewords.append(bytearray([len(qr["data"])]), __get_character_count_length(qr["mode"], qr["version"]))
    codewords.append(bytearray(qr["data"].encode(encoding="ascii")), len(qr["data"]) * 8)
    codewords.pad_bytes(TOTAL_NUMBER_OF_CODEWORDS[qr["version"]] - NUMBER_OF_EC_CODEWORDS[qr["version"]][qr["error_correction_level"].value])
    codewords.append(__get_error_correction_codewords(codewords, TOTAL_NUMBER_OF_CODEWORDS[qr["version"]]),
                     NUMBER_OF_EC_CODEWORDS[qr["version"]][qr["error_correction_level"].value] * 8)
    __insert_format_information(qr)
    __populate_matrix(qr,codewords)

    fill = [1, 0]
    while fill is not None:
        fill = __put_module(qr, fill, 0)

    __apply_mask(qr)
    __insert_alignment_patterns(qr)  # TODO: think of a way to avoid masking it without redrawing


def __get_character_count_length(mode: Mode, version: int):
    if mode == Mode.NUMERIC:  # numeric mode
        return 10 if version < 10 else 12 if version < 27 else 14
    if mode == Mode.ALPHANUMERIC:  # alphanumeric mode
        return 9 if version < 10 else 11 if version < 27 else 13
    if mode == Mode.BYTE:  # byte mode
        return 8 if version < 10 else 16
    if mode == Mode.KANJI:  # kanji mode
        return 8 if version < 10 else 10 if version < 27 else 12

def __insert_function_patterns(qr: QRCode):
    __insert_finder_patterns(qr)
    __insert_separators(qr)
    __insert_timing_patterns(qr)
    __insert_alignment_patterns(qr)

def __insert_finder_patterns(qr: QRCode):
    for pos in [(0, 0), (0, qr.get_width() - 7), (qr.get_width() - 7, 0)]:
        for x in range(7):
            for y in range(7):
                if (1 <= x < 6 and 1 <= y < 6) and (x < 2 or x >= 5 or y < 2 or y >= 5):
                    qr["matrix"][pos[0] + x][pos[1] + y] = 0
                else:
                    qr["matrix"][pos[0] + x][pos[1] + y] = 1

def __insert_separators(qr: QRCode):
    for i in range(8):
        qr["matrix"][i][7] = 0
        qr["matrix"][7][i] = 0

        qr["matrix"][i][qr.get_width() - 7 - 1] = 0
        qr["matrix"][7][qr.get_width() - i - 1] = 0

        qr["matrix"][qr.get_width() - i - 1][7] = 0
        qr["matrix"][qr.get_width() - 7 - 1][i] = 0

def __insert_timing_patterns(qr: QRCode):
    for i in range(8, qr.get_width() - 7):
        qr["matrix"][6][i] = (i + 1) % 2
        qr["matrix"][i][6] = (i + 1) % 2

def __insert_alignment_patterns(qr: QRCode):
    if qr["version"]==1:
        return
    grid_size = qr["version"] // 7 + 2
    spacing = (qr.get_width() - 12) // (grid_size - 1)
    for x in range(grid_size):
        for y in range(grid_size):
            if x == 0 and y == 0:
                continue
            if x == grid_size - 1 and y == 0:
                continue
            if x == 0 and y == grid_size - 1:
                continue
            for i in range(-2, 3):
                for j in range(-2, 3):
                    qr["matrix"][5 + x * spacing + i][5 + y * spacing + j] = 1 if (
                            i == -2 or i == 2 or j == -2 or j == 2 or (i == 0 and j == 0)) else 0

def __insert_format_information(qr: QRCode):
    format_information = []
    format_information.append(qr["error_correction_level"].value>>1)
    format_information.append(qr["error_correction_level"].value&1)

    format_information.append((qr["mask"] >> 2) & 1)
    format_information.append((qr["mask"] >> 1) & 1)
    format_information.append((qr["mask"]) & 1)

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
        qr["matrix"][8][i] = format_information[i]
        qr["matrix"][qr.get_width() - 1 - i][8] = format_information[i]

    qr["matrix"][8][7] = format_information[6]
    qr["matrix"][8][8] = format_information[7]
    qr["matrix"][7][8] = format_information[8]

    qr["matrix"][qr.get_width() - 1 - 6][8] = format_information[6]
    qr["matrix"][qr.get_width() - 1 - 7][8] = format_information[7]
    qr["matrix"][8][qr.get_width() - 1 - 6] = format_information[8]

    for i in range(9, 15):
        qr["matrix"][14 - i][8] = format_information[i]
        qr["matrix"][8][qr.get_width() - 1 - 14 + i] = format_information[i]

    qr["matrix"][8][qr.get_width() - 1 - 7] = 1

def __populate_matrix(qr: QRCode, codewords: Bitarray):
    ba = codewords.get_bytearray()
    coords = [qr.get_width() - 1, qr.get_width() - 1]

    for b in range((8 - (len(codewords) % 8)) % 8, 8):
        value = (ba[0] << b & 128) >> 7
        coords = __put_module(qr, coords, value)
        continue

    for B in range(1, len(ba)):
        for b in range(8):
            value = (ba[B] << b & 128) >> 7
            coords = __put_module(qr, coords, value)
            if coords is None:
                print(qr["matrix"])
                print(len(qr["matrix"]))
                print(matrix_to_str(qr))
                raise ValueError("Could not find a place to put a module. " + str(len(ba) - B) + "B " + str(
                    8 - b) + "b remaining.")

def __put_module(qr: QRCode, coords: list, value: int):
    """
    Tries to put module in specified coordinates.
    :param coords: coords at which to try to place value
    :param value: value to put
    :return: coordinate at which the function succeeded or None if failed
    """
    if not isinstance(coords, list) and len(coords) != 2:
        raise ValueError("coords must be a list of length two")

    while qr["matrix"][coords[0]][coords[1]] is not None:
        # 1 if up, -1 if down, and 0 if left
        direction = 1 - coords[0] % 2 if coords[0] < 6 else coords[0] % 2
        if direction != 0 and ((coords[0] - qr.get_width() - 1) // 2) % 2 != 0:
            direction *= -1

        coords[1] -= direction
        coords[0] += -1 if direction == 0 else 1
        if coords[1] < 0:
            coords[1] = 0
            coords[0] -= 2
        elif coords[1] >= qr.get_width():
            coords[1] = qr.get_width() - 1
            coords[0] -= 2
        if coords[0] < 0:
            return None

    qr["matrix"][coords[0]][coords[1]] = value

    return coords

def matrix_to_str(qr:QRCode):
    out = ""
    for y in range(-4, qr.get_width() + 4):
        for x in range(-4, qr.get_width() + 4):
            if x < 0 or x >= qr.get_width() or y < 0 or y >= qr.get_width():
                out += "\x1b[107m \x1b[0m"
                continue
            val = qr["matrix"][x][y]
            if val is None:
                out += "?"  # this is purely for debugging purposes
            elif val == 0:
                out += "\x1b[107m \x1b[0m"
            else:
                out += "\x1b[40m \x1b[0m"

        out += '\n'

    return out

def __is_in_functional_patterns(qr: QRCode, x: int, y: int):
    """
    Checks if module at (x,y) is a part of functional_patterns. The left upper corner has coordinates of (0,0)
    """
    if (x < 9 and y < 9):  # left square
        return True
    if (x > qr.get_width() - 9 and y < 9):  # right square
        return True
    if (x < 9 and y > qr.get_width() - 9):  # bottom square
        return True
    if x == 6 or y == 6:  # timing strips
        return True
    return False

def __apply_mask(qr: QRCode):
    for i in range(qr.get_width()):
        for j in range(qr.get_width()):
            if __is_in_functional_patterns(qr, j, i):
                continue
            if MASKS[qr["mask"]](i, j):
                if qr["matrix"][j][i] is None:
                    continue
                qr["matrix"][j][i] += 1
                qr["matrix"][j][i] %= 2

# https://dev.to/maxart2501/let-s-develop-a-qr-code-generator-part-iii-error-correction-1kbm
def __get_error_correction_codewords(data_codewords: self.Bitarray, total_length):
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


class QRCode(dict):

    def __init__(self):
        super().__init__([
            ("mode", Mode.BYTE),
            ("data", "i'm having a boiby"),
            ("error_correction_level", ErrorCorrectionLevel.M),
            ("mask", 2),
            ("version", None),
            ("matrix", [])
        ])

    def __getitem__(self, key):
        match key:
            case "version":
                if key== "version" and dict.__getitem__(self, key) is None:
                    self["version"] = get_minimal_version(self["mode"],self["data"],self["error_correction_level"])
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        match key:
            case "mode":
                if isinstance(value, Mode):
                    dict.__setitem__(self, "mode", value)
                elif isinstance(value, int):
                    dict.__setitem__(self, "mode", Mode(value))
            case "data":
                dict.__setitem__(self, "data", value)
            case "error_correction_level" | "ecl":
                if isinstance(value, ErrorCorrectionLevel):
                    dict.__setitem__(self, "error_correction_level", value)
                elif isinstance(value, int):
                    dict.__setitem__(self, "error_correction_level", ErrorCorrectionLevel(value))
            case "mask":
                if 0<=value<8:
                    dict.__setitem__(self, "mask", value)
                else:
                    raise ValueError("Mask should have a value [0;8)")
            case "version":
                if value is None:
                    dict.__setitem__(self, "version", get_minimal_version(self["mode"], self["data"], self["error_correction_level"]))
                elif 0<value<=40:
                    dict.__setitem__(self, "version", value)
                else:
                    raise ValueError("Version should be a number in [1;40] or None for smallest version containing specified data")
        dict.__setitem__(self, key, value)

    def get_width(self):
        return 17 + 4 * self["version"]

    def update_matrix(self):
        update_matrix(self)
        # print(self["matrix"])
        # print(Bitarray.from_boolean_matrix(self["matrix"]))
        # print(Bitarray.from_boolean_matrix(self["matrix"]).to_boolean_matrix())
        # self["matrix"]=Bitarray.from_boolean_matrix(self["matrix"]).to_boolean_matrix()