from typing import Dict, Any
from api.repositories.book.book_repository import BookRepository


def reactivate_book(book_id: int) -> Dict[str, Any]:
    book_dict: Dict[str, Any] = BookRepository.reactivate_book(book_id)
    return {
        'id': book_dict['id'],
        'title': book_dict['title'],
        'author': book_dict['author'],
        'category': book_dict['category'],
        'bar_code': book_dict['bar_code'],
        'barcode_download_url': book_dict['barcode_download_url'],
        'total_copies': book_dict['total_copies'],
        'available_copies': book_dict['available_copies'],
        'created_at': book_dict['created_at'].strftime('%d/%m/%Y %H:%M:%S'),
        'status': 'active' if book_dict['active'] else 'inactive'
    }
