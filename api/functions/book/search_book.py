from typing import Dict
from api.repositories.book.book_repository import BookRepository


def search_books_by_title(title, page=1, per_page=10) -> Dict:
    result = BookRepository.get_books_by_field(
        'title', title, page=page, per_page=per_page)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }


def search_books_by_author(author, page=1, per_page=10) -> Dict:
    result = BookRepository.get_books_by_field(
        'author', author, page=page, per_page=per_page)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }


def search_books_by_category(category, page=1, per_page=10) -> Dict:
    result = BookRepository.get_books_by_field(
        'category', category, page=page, per_page=per_page)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }


def search_books_by_barcode(barcode, page=1, per_page=10) -> Dict:
    result = BookRepository.get_books_by_field(
        'barcode', barcode, page=page, per_page=per_page)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }


def search_books_by_date_range(start_date, end_date, page=1, per_page=10) -> Dict:
    result = BookRepository.get_books_by_field(
        'date_range', (start_date, end_date), page=page, per_page=per_page)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }


def get_active_books(page=1, per_page=10) -> Dict:
    result = BookRepository.get_books_by_field(
        'active', True, page=page, per_page=per_page)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }


def get_inactive_books(page=1, per_page=10) -> Dict:
    result = BookRepository.get_books_by_field(
        'active', False, page=page, per_page=per_page)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }


def search_book_by_id(book_id) -> Dict:
    result = BookRepository.get_books_by_field('id', book_id)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }


def get_all_books(page=1, per_page=10) -> Dict:
    result = BookRepository.get_all_books(page=page, per_page=per_page)
    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': result['items']
    }
