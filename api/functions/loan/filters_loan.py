from typing import Dict, Union, List
from api.repositories.loan.loan_repository import LoanRepository


def get_loans_by_field(field: str, value: str, page: int = 1, per_page: int = 10) -> Dict:
    result = LoanRepository.get_loans_by_field(field, value, page, per_page)
    loan_list = []

    if isinstance(result['items'], list):
        for loan in result['items']:
            loan_data = {
                'id': loan['id'],
                'student_id': loan['student_id'],
                'book_id': loan['book_id'],
                'loan_date': loan['loan_date'],
                'return_date': loan['return_date'],
                'returned': loan['returned']
            }
            loan_list.append(loan_data)

    return {
        'page': result['page'],
        'per_page': result['per_page'],
        'total_pages': result['total_pages'],
        'total_items': result['total_items'],
        'items': loan_list if loan_list else result['items']
    }
