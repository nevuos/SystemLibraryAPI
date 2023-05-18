from typing import Dict
from api.repositories.loan.loan_repository import LoanRepository


def update_loan(loan_id, student_id=None, book_id=None, return_date=None, returned=None) -> Dict:
    return LoanRepository.update(loan_id, student_id, book_id, return_date, returned)
