from flask import make_response
from flask_jwt_extended import jwt_required
from api.functions.download.download_function import download_function
from api.utils.handlers.error_handlers import handle_errors


@jwt_required()
@handle_errors
def download_image_handler(bar_code):
    barcode_img_bytes = download_function(bar_code)

    response = make_response(barcode_img_bytes)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition',
                        f'attachment; filename="{bar_code}.png"')
    return response
