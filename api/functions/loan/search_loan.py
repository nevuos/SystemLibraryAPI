from typing import Dict
from flask import jsonify
from api.repositories.loan.loan_repository import LoanRepository


def search_loan_by_id(loan_id) -> Dict:
    return LoanRepository.get_loans_by_field('id', loan_id)


def search_loans_by_student_id(student_id) -> Dict:
    return LoanRepository.get_loans_by_field('student_id', student_id)


def search_loans_by_book_id(book_id) -> Dict:
    return LoanRepository.get_loans_by_field('book_id', book_id)


def search_loans_by_return_status(returned) -> Dict:
    return LoanRepository.get_loans_by_field('returned', returned)


def search_loans_by_return_date_range(start_date, end_date) -> Dict:
    return LoanRepository.get_loans_by_field('return_date', (start_date, end_date))


def search_loans_by_loan_date_range(start_date, end_date) -> Dict:
    return LoanRepository.get_loans_by_field('loan_date', (start_date, end_date))


def get_all_loans() -> Dict:
    return LoanRepository.get_all_loans()
