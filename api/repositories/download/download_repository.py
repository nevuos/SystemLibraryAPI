from api.models.book import Book


class BookNotFoundError(Exception):
    pass


def get_book_by_bar_code(bar_code: int) -> Book:
    book = Book.query.filter_by(bar_code=bar_code).first()

    if book is None:
        raise BookNotFoundError(f"No book found with bar code {bar_code}")

    return book
