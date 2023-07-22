from flask import Blueprint
from api.request_handlers.download.download_handler import download_image_handler
from api.utils.configurations.extensions import limiter

download_bp = Blueprint('download_routes', __name__)


@download_bp.route('/download_image_barcode/<int:bar_code>', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def download_image_barcode(bar_code):
    return download_image_handler(bar_code)
