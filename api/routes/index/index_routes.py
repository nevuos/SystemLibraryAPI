from flask import Blueprint, jsonify
from ...utils.api_info.api_info import api_info

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    return jsonify(api_info)
