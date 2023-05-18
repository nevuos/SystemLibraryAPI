from barcode import Code128  # type: ignore
from barcode.writer import ImageWriter  # type: ignore
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from api.utils.cache.cache import redis_cache
from typing import Optional


def generate_barcode(code, category, font_size=30, dpi=300, barcode_width=400) -> BytesIO:
    cached_data: Optional[bytes] = redis_cache.get(code)

    if cached_data is not None:
        return BytesIO(cached_data)

    writer = ImageWriter()
    writer.set_options({"compress_level": 0})

    bar_code = Code128(str(code), writer=writer)

    barcode_io = BytesIO()
    bar_code.write(barcode_io)
    barcode_io.seek(0)
    barcode_img = Image.open(barcode_io)

    wpercent = (barcode_width / float(barcode_img.size[0]))
    hsize = int((float(barcode_img.size[1]) * float(wpercent)))
    barcode_img = barcode_img.resize((barcode_width, hsize), Image.ANTIALIAS)

    new_img_height = barcode_img.height + 30
    new_img = Image.new('RGB', (barcode_img.width, new_img_height), 'white')
    draw = ImageDraw.Draw(new_img)

    font = ImageFont.truetype('arial', font_size)
    text_width, text_height = draw.textsize(category, font=font)

    text_x = (new_img.width - text_width) // 2
    text_y = 10

    draw.text((text_x, text_y), category, fill='black', font=font)

    new_img.paste(barcode_img, (0, text_height + 20))

    a4_img = Image.new('RGB', (int(8.27 * dpi), int(11.69 * dpi)), 'white')

    a4_img.paste(new_img, (0, 0))

    img_byte_arr = BytesIO()
    a4_img.save(img_byte_arr, format='PNG', optimize=True)
    img_byte_arr.seek(0)

    redis_cache.set(code, img_byte_arr.getvalue(), ex=3600)

    return img_byte_arr
