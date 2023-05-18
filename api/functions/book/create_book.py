from typing import Dict
from api.repositories.book.book_repository import BookRepository


def create_book(title: str, author: str, category: str) -> Dict:
    book = BookRepository.create(title, author, category)
    response = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category': book.category,
        'bar_code': book.bar_code,
        'barcode_download_url': book.barcode_download_url,
        'created_at': book.created_at.strftime('%d/%m/%Y %H:%M:%S')
    }
    return response
