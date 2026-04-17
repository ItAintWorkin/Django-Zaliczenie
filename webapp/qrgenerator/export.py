from PIL import Image
from qrgenerator.qrcode import QRCode
import base64
from io import BytesIO


def as_jpg_base64(qr: QRCode, module_size=16):
    img = Image.new("1", ((qr.get_width() + 8), (qr.get_width() + 8)), 1)

    qr_matrix = qr["matrix"]
    for x in range(qr.get_width()):
        for y in range(qr.get_width()):
            img.putpixel((x+4,y+4), 0 if qr_matrix[x][y] != 0 else 1)

    img = img.resize(((qr.get_width() + 8) * module_size, (qr.get_width() + 8) * module_size))

    buffer = BytesIO()
    img.save(buffer, format="JPEG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def as_bytearray(qr: QRCode):
    array = bytearray()
    qr_matrix = qr["matrix"]
    byte_buffer = 0
    bit_count = 0
    i=0
    for x in range(qr.get_width()):
        for y in range(qr.get_width()):
            i +=1
            byte_buffer |= 0 if qr_matrix[x][y] == 0 else 1<<(7-bit_count)
            print("0" if qr_matrix[x][y] != 0 else "1", end="")
            bit_count += 1
            if bit_count == 8:
                array.append(byte_buffer)
                bit_count = 0
                byte_buffer = 0
    print("\n"+array.hex())
    return array
