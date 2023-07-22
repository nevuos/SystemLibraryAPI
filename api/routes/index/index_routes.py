from flask import Blueprint, jsonify
from ...utils.api_info.api_info import api_info
from api.utils.configurations.extensions import limiter


index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def index():
    return jsonify(api_info)
