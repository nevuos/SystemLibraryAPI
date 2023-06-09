from flask import Blueprint
from api.request_handlers.book.book_handlers import (
    handle_create_book_request,
    handle_deactivate_book_request,
    handle_get_books_request,
    handle_reactivate_book_request,
    handle_search_books_by_bar_code_request,
    handle_search_books_by_title_request,
    handle_search_books_by_author_request,
    handle_search_books_by_category_request,
    handle_get_book_by_id_request,
    handle_update_book_request,
    handle_get_books_by_date_range_request,
    handle_get_inactive_books_request,
    handle_get_active_books_request,
    handle_get_all_books_request,
)

book_bp = Blueprint('book_routes', __name__)


@book_bp.route('/books', methods=['POST'])
def create_book():
    return handle_create_book_request()


@book_bp.route('/books/<int:book_id>/deactivate', methods=['POST'])
def deactivate_book(book_id):
    return handle_deactivate_book_request(book_id)


@book_bp.route('/books', methods=['GET'])
def get_books():
    return handle_get_books_request()


@book_bp.route('/books/<int:book_id>/reactivate', methods=['POST'])
def reactivate_book(book_id):
    return handle_reactivate_book_request(book_id)


@book_bp.route('/books/search/title', methods=['GET'])
def search_books_by_title():
    return handle_search_books_by_title_request()


@book_bp.route('/books/search/author', methods=['GET'])
def search_books_by_author():
    return handle_search_books_by_author_request()


@book_bp.route('/books/search/category', methods=['GET'])
def search_books_by_category():
    return handle_search_books_by_category_request()


@book_bp.route('/books/search/barcode', methods=['GET'])
def search_books_by_code():
    return handle_search_books_by_bar_code_request()


@book_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    return handle_get_book_by_id_request(book_id)


@book_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    return handle_update_book_request(book_id)


@book_bp.route('/books/search/date', methods=['GET'])
def search_books_by_date_range():
    return handle_get_books_by_date_range_request()


@book_bp.route('/books/inactive', methods=['GET'])
def get_inactive_books():
    return handle_get_inactive_books_request()


@book_bp.route('/books/active', methods=['GET'])
def get_active_books():
    return handle_get_active_books_request()


@book_bp.route('/books/all', methods=['GET'])
def get_all_books():
    return handle_get_all_books_request()
