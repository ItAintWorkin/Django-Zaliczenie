from PIL import Image
from qrgenerator.qrcode import QRCode
import base64
from io import BytesIO


def get_base64(text: str, module_size=16):
    qr = QRCode(text)
    img = Image.new("1", ((qr.get_width() + 8), (qr.get_width() + 8)), 1)

    qr_matrix = qr.build()
    for x in range(qr.get_width()):
        for y in range(qr.get_width()):
            img.putpixel((x+4,y+4), 0 if qr_matrix[x][y] != 0 else 1)

    img = img.resize(((qr.get_width() + 8) * module_size, (qr.get_width() + 8) * module_size))

    buffer = BytesIO()
    img.save(buffer, format="JPEG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")
