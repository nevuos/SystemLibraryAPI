from typing import Dict
from api.models.book import Book
from api.repositories.book.book_repository import BookRepository


def update_book(book_id, title, author, category) -> Dict:
    book = BookRepository.update_book(book_id, title, author, category)
    return {
        'id': book['id'],
        'title': book['title'],
        'author': book['author'],
        'category': book['category']
    }
