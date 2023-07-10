from flask import request, jsonify
from api.functions.book.create_book import create_book
from api.functions.book.deactivate_book import deactivate_book
from api.functions.book.reactivate_book import reactivate_book
from api.functions.book.update_book import update_book
from api.functions.book.search_book import (
    search_books_by_title,
    search_books_by_author,
    search_books_by_category,
    search_books_by_barcode,
    search_books_by_date_range,
    get_active_books,
    get_inactive_books,
    search_book_by_id,
    get_all_books,
)
from api.utils.validators.generic.validate_required import validate_required_fields
from api.utils.handlers.error_handlers import handle_errors


@handle_errors
@validate_required_fields(['title', 'author', 'category', 'total_copies'])
def handle_create_book_request():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    category = data.get('category')
    total_copies = data.get('total_copies')

    response_data = create_book(title, author, category, total_copies)
    response_data['message'] = 'Livro cadastrado com sucesso'
    return jsonify(response_data), 201


@handle_errors
def handle_deactivate_book_request(book_id):
    response_data = deactivate_book.deactivate_book(book_id)
    response_data['message'] = 'Livro desativado com sucesso'
    return jsonify(response_data), 200


@handle_errors
def handle_get_books_request():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = get_all_books(page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200


@handle_errors
def handle_reactivate_book_request(book_id):
    response_data = reactivate_book.reactivate_book(book_id)
    response_data['message'] = 'Livro reativado com sucesso'
    return jsonify(response_data), 200


@handle_errors
def handle_search_books_by_title_request():
    title = request.args.get('title')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = search_books_by_title(title, page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200


@handle_errors
def handle_search_books_by_author_request():
    author = request.args.get('author')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = search_books_by_author(author, page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200


@handle_errors
def handle_search_books_by_category_request():
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = search_books_by_category(category, page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200


@handle_errors
def handle_search_books_by_bar_code_request():
    bar_code = request.args.get('bar_code')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = search_books_by_barcode(bar_code, page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200


@handle_errors
def handle_get_book_by_id_request(book_id):
    response_data = search_book_by_id(book_id)
    response_data['message'] = 'Livro recuperado com sucesso'
    return jsonify(response_data), 200


@handle_errors
def handle_update_book_request(book_id):
    data = request.get_json()
    response_data = update_book.update_book(book_id, data.get(
        'title'), data.get('author'), data.get('category'), data.get('total_copies'))
    response_data['message'] = 'Livro atualizado com sucesso'
    return jsonify(response_data), 200


@handle_errors
def handle_get_books_by_date_range_request():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = search_books_by_date_range(start_date, end_date, page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200


@handle_errors
def handle_get_inactive_books_request():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = get_inactive_books(page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200


@handle_errors
def handle_get_active_books_request():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = get_active_books(page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200


@handle_errors
def handle_get_all_books_request():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = get_all_books(page, per_page)
    return jsonify({'message': 'Livros recuperados com sucesso', 'books': books}), 200
