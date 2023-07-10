from typing import Dict
from api.repositories.book.book_repository import BookRepository


def create_book(title: str, author: str, category: str, total_copies: int) -> Dict:
    book = BookRepository.create(title, author, category, total_copies)
    response = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': book.category,
        'bar_code': book.bar_code,
        'barcode_download_url': book.barcode_download_url,
        'total_copies': book.total_copies,
        'available_copies': book.available_copies,
        'created_at': book.created_at.strftime('%d/%m/%Y %H:%M:%S')
    }
    return response
