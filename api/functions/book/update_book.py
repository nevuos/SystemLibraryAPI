from typing import Dict
from api.models.book import Book
from api.repositories.book.book_repository import BookRepository


def update_book(book_id: int, title: str, author: str, category: str, total_copies: int) -> Dict:
    book = BookRepository.update_book(book_id, title, author, category, total_copies)
    return {
        'id': book['id'],
        'title': book['title'],
        'author': book['author'],
        'category': book['category'],
        'total_copies': book['total_copies'],
        'available_copies': book['available_copies']
    }
