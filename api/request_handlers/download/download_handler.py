from flask import make_response
from api.utils.functions.barcode_function import generate_barcode
from api.repositories.download.download_repository import get_book_by_bar_code
from api.request_handlers.errors.error_handlers import handle_errors


@handle_errors
def download_image_handler(bar_code):
    book = get_book_by_bar_code(bar_code)

    barcode_img = generate_barcode(bar_code, book.category)
    barcode_img_bytes = barcode_img.getvalue()

    response = make_response(barcode_img_bytes)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition',
                         f'attachment; filename="{bar_code}.png"')
    return response
