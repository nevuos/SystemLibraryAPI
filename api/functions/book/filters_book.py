from typing import Dict, Any
from api.repositories.book.book_repository import BookRepository


def get_books_by_field(field, value, page=1, per_page=10, active=True) -> Dict[str, Any]:
    result = BookRepository.get_books_by_field(field, value, page, per_page, active)
    book_list = []

    for book in result['items']:
        book_data = {
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'category': book['category'],
            'bar_code': book['bar_code'],
            'barcode_download_url': book['bar_code_url'],
            'created_at': book['created_at'],
            'status': 'active' if book['status'] == 'active' else 'inactive'
        }
        book_list.append(book_data)

    response = {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': book_list
    }

    return response
