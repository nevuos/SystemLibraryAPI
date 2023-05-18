from barcode import Code128  # type: ignore
from barcode.writer import ImageWriter  # type: ignore
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def generate_barcode(code, category) -> BytesIO:
    writer = ImageWriter()
    bar_code = Code128(str(code), writer=writer)

    barcode_io = BytesIO()
    bar_code.write(barcode_io)
    barcode_io.seek(0)
    barcode_img = Image.open(barcode_io)

    new_img = Image.new('RGB', (barcode_img.width, barcode_img.height + 30), 'white')
    draw = ImageDraw.Draw(new_img)

    font = ImageFont.truetype('arial', 15)
    draw.text((0, 0), category, fill='black', font=font)

    new_img.paste(barcode_img, (0, 30))

    img_byte_arr = BytesIO()
    new_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr
