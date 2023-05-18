from typing import Any, Dict
import pytz
from flask import url_for
from datetime import datetime
from api.models.book import Book
from api.models.code_sequence import CodeSequence
from api.utils.configurations.extensions import db
from api.utils.functions.barcode_function import generate_barcode
from api.utils.cache.cache import cache


class BookNotFoundError(Exception):
    pass


class BookRepository:
    @staticmethod
    def create(title, author, category, total_copies) -> Book:
        if total_copies <= 0:
            raise ValueError("Total copies must be a positive integer.")

        with db.session.begin_nested():
            code_sequence = CodeSequence.query.with_for_update().first()
            if code_sequence is None:
                code_sequence = CodeSequence(id=1)
                db.session.add(code_sequence)
            bar_code = code_sequence.id
            code_sequence.id += 1

        db.session.commit()

        barcode_download_url = url_for(
            'download_routes.download_image_barcode', bar_code=bar_code, _external=True)

        brt_timezone = pytz.timezone('America/Sao_Paulo')
        created_at = datetime.now(brt_timezone)

        book = Book(
            title=title,
            bar_code=bar_code,
            author=author,
            category=category,
            barcode_download_url=barcode_download_url,
            created_at=created_at,
            total_copies=total_copies,
            available_copies=total_copies
        )
        db.session.add(book)
        db.session.commit()

        if not book or book.total_copies != total_copies:
            raise BookNotFoundError(
                f"Book {title} by {author} in {category} with total copies {total_copies} could not be created.")

        return book


    @staticmethod
    def deactivate_book(book_id) -> dict:
        book = Book.query.get(book_id)
        if book is None:
            raise BookNotFoundError(f"No book found with id {book_id}")

        book.active = False
        brt_timezone = pytz.timezone('America/Sao_Paulo')
        book.deactivated_at = datetime.now(brt_timezone)
        db.session.commit()
        return {'deactivated_at': book.deactivated_at.strftime('%d/%m/%Y %H:%M:%S')}

    @staticmethod
    @cache.cached(timeout=300)
    def get_books_by_field(field, value, page=1, per_page=10, active=True) -> dict:
        query = Book.query.filter(getattr(Book, field).ilike(f'%{value}%'))

        if active is not None:
            query = query.filter(Book.active == active)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        books = pagination.items

        book_list = [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'bar_code': book.bar_code,
            'bar_code_url': book.barcode_download_url,
            'created_at': book.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'active' if book.active else 'inactive'
        } for book in books]

        return {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'items': book_list
        }

    @staticmethod
    def reactivate_book(book_id: int) -> Dict[str, Any]:
        book = Book.query.get(book_id)

        if not book:
            raise BookNotFoundError(f"No book found with id {book_id}")

        book.active = True
        book.deactivated_at = None
        db.session.commit()

        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'bar_code': book.bar_code,
            'barcode_download_url': book.barcode_download_url,
            'created_at': book.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            'status': 'active' if book.active else 'inactive'
        }

    @staticmethod
    def update_book(book_id, title, author, category) -> dict:
        book = Book.query.get(book_id)
        if book is None:
            raise BookNotFoundError(f"No book found with id {book_id}")

        book.title = title
        book.author = author
        book.category = category
        db.session.commit()
        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category
        }

    @staticmethod
    def get_all_books(page=1, per_page=10) -> dict:
        result = BookRepository.get_books_by_field(
            'title', '', page=page, per_page=per_page, active=None)
        book_list = []

        for book in result['items']:
            book_data = {
                'id': book['id'],
                'title': book['title'],
                'author': book['author'],
                'category': book['category'],
                'bar_code': book['bar_code'],
                'bar_code_url': book['bar_code_url'],
                'created_at': book['created_at'],
                'status': book['status']
            }
            book_list.append(book_data)

        return {
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages'],
            'total_items': result['total_items'],
            'items': book_list
        }
