from typing import Dict, Any
from api.repositories.book.book_repository import BookRepository


def deactivate_book(book_id) -> Dict[str, Any]:
    result = BookRepository.deactivate_book(book_id)
    response = {
        'message': result['message'],
        'deactivated_at': result['deactivated_at']
    }
    return response
