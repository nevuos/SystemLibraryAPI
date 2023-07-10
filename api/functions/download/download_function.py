from api.repositories.download.download_repository import get_book_by_bar_code
from api.utils.functions.barcode.barcode_function import generate_barcode
from api.utils.handlers.error_handlers import handle_errors


@handle_errors
def download_function(bar_code):
    book = get_book_by_bar_code(bar_code)
    barcode_img = generate_barcode(bar_code, book.category)
    return barcode_img.getvalue()
