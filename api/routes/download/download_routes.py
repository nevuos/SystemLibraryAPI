from flask import Blueprint
from flask_jwt_extended import jwt_required
from api.request_handlers.download.download_handler import download_image_handler

download_bp = Blueprint('download_routes', __name__)


@jwt_required
@download_bp.route('/download_image_barcode/<int:bar_code>')
def download_image_barcode(bar_code):
    return download_image_handler(bar_code)
