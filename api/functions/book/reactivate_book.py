from typing import Any, Dict
from api.repositories.book.book_repository import BookRepository


def reactivate_book(book_id) -> Dict[str, Any]:
    book = BookRepository.reactivate_book(book_id)
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': book.category,
        'bar_code': book.bar_code,
        'barcode_download_url': book.barcode_download_url,
        'created_at': book.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        'status': 'active' if book.status == 'active' else 'inactive'
    }
