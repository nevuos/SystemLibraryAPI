import pytz
from api.utils.configurations.extensions import db
from datetime import datetime, timedelta
from api.models.loan import Loan
from api.models.book import Book
from api.models.student import Student
from api.utils.functions.holiday.holiday_function import is_business_day
from api.utils.cache.cache import cache
from typing import List, Dict, Any, Union, Optional


class LoanNotFoundError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class StudentNotFoundError(Exception):
    pass


class LoanRepository:

    @staticmethod
    def create(student_id: int, book_id: int) -> Dict[str, Union[int, Dict[str, str], datetime]]:
        student = Student.query.get(student_id)
        book = Book.query.get(book_id)

        if not student:
            raise StudentNotFoundError(f"No student found with id {student_id}")
        if not student.active:  # Verificar se o estudante está ativo
            raise ValueError("Student is inactive. Cannot create loan.")

        if not book:
            raise BookNotFoundError(f"No book found with id {book_id}")
        if not book.active:  # Verificar se o livro está ativo
            raise ValueError("Book is inactive. Cannot create loan.")

        if book.available_copies <= 0:
            raise ValueError("No available copies of the book.")

        new_loan = Loan(student_id=student_id, book_id=book_id)
        db.session.add(new_loan)
        book.available_copies -= 1
        db.session.commit()

        receipt = {
            'id': new_loan.id,
            'student': {'name': student.name, 'registration_number': student.registration_number},
            'book': {'title': book.title, 'author': book.author, 'category': book.category},
            'loan_date': new_loan.loan_date,
            'return_date': new_loan.return_date
        }
        return receipt

    @staticmethod
    def deactivate_loan(loan_id: int) -> Dict[str, str]:
        loan = Loan.query.get(loan_id)

        if not loan:
            raise LoanNotFoundError(f"No loan found with id {loan_id}")

        loan.returned = True
        brt_timezone = pytz.timezone('America/Sao_Paulo')
        loan.deactivated_at = datetime.now(brt_timezone)
        db.session.commit()

        book = Book.query.get(loan.book_id)
        book.available_copies += 1
        db.session.commit()

        return {'deactivated_at': loan.deactivated_at.strftime('%d/%m/%Y %H:%M:%S')}

    @staticmethod
    def reactivate_loan(loan_id: int) -> Dict[str, Any]:
        loan = Loan.query.get(loan_id)

        if not loan:
            raise LoanNotFoundError(f"No loan found with id {loan_id}")

        loan.active = True
        loan.deactivated_at = None
        db.session.commit()

        brt_timezone = pytz.timezone('America/Sao_Paulo')
        reactivated_at = datetime.now(brt_timezone)

        return {
            'id': loan.id,
            'student_id': loan.student_id,
            'book_id': loan.book_id,
            'loan_date': loan.loan_date.strftime('%d/%m/%Y %H:%M:%S'),
            'return_date': loan.return_date.strftime('%d/%m/%Y %H:%M:%S') if loan.return_date else None,
            'returned': loan.returned,
            'reactivated_at': reactivated_at.strftime('%d/%m/%Y %H:%M:%S')
        }

    @staticmethod
    @cache.memoize(timeout=300)
    def return_loan(loan_id: int) -> Dict[str, Union[str, float]]:
        loan = Loan.query.get(loan_id)

        if loan is None:
            raise LoanNotFoundError(f"No loan found with id {loan_id}")
        if loan.returned:
            raise ValueError("O livro já foi devolvido.")

        return_date = loan.return_date

        while not is_business_day(return_date):
            return_date += timedelta(days=1)

        days_overdue = (datetime.utcnow() - return_date).days

        fine = 0.0
        if days_overdue > 7:
            fine = (days_overdue - 7) * 0.50

        loan.returned = True
        db.session.commit()

        book = Book.query.get(loan.book_id)
        book.available_copies += 1
        db.session.commit()

        return {
            'message': 'Livro devolvido com sucesso.',
            'fine': fine
        }

    @staticmethod
    def get_loans_by_field(field: str, value: Any, page=1, per_page=10) -> Dict[str, Union[int, List[Dict[str, Union[int, str, bool]]]]]:
        if field == 'student_id':
            query = Loan.query.filter(Loan.student_id == value)
        elif field == 'book_id':
            query = Loan.query.filter(Loan.book_id == value)
        else:
            raise ValueError("Campo inválido.")

        pagination = query.paginate(page=page, per_page=per_page)
        loans = pagination.items

        loan_list = [{
            'id': loan.id,
            'student_id': loan.student_id,
            'book_id': loan.book_id,
            'loan_date': loan.loan_date.strftime('%d/%m/%Y'),
            'return_date': loan.return_date.strftime('%d/%m/%Y'),
            'returned': loan.returned
        } for loan in loans]

        return {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'items': loan_list
        }

    @staticmethod
    @cache.cached(timeout=300)
    def get_all_loans(page=1, per_page=10) -> Dict[str, Union[int, List[Dict[str, Union[int, str, bool]]]]]:
        pagination = Loan.query.paginate(page=page, per_page=per_page)
        loans = pagination.items

        loan_list = [{
            'id': loan.id,
            'student_id': loan.student_id,
            'book_id': loan.book_id,
            'loan_date': loan.loan_date.strftime('%d/%m/%Y'),
            'return_date': loan.return_date.strftime('%d/%m/%Y'),
            'returned': loan.returned
        } for loan in loans]

        return {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'items': loan_list
        }

    @staticmethod
    def update(loan_id: int, student_id: Optional[int] = None, book_id: Optional[int] = None,
               return_date: Optional[datetime] = None, returned: Optional[bool] = None) -> Dict[str, Union[str, int, datetime, bool]]:
        loan = Loan.query.get(loan_id)

        if loan is None:
            raise LoanNotFoundError(f"No loan found with id {loan_id}")

        if student_id is not None:
            loan.student_id = student_id
        if book_id is not None:
            loan.book_id = book_id
        if return_date is not None:
            loan.return_date = return_date
        if returned is not None:
            loan.returned = returned

        db.session.commit()

        return {
            'message': f'Loan {loan_id} updated successfully.',
            'loan_id': loan.id,
            'student_id': loan.student_id,
            'book_id': loan.book_id,
            'loan_date': loan.loan_date,
            'return_date': loan.return_date,
            'returned': loan.returned
        }
