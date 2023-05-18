from typing import Dict, Any
from api.repositories.loan.loan_repository import LoanRepository


def reactivate_loan(loan_id) -> Dict[str, Any]:
    loan_dict: Dict[str, Any] = LoanRepository.reactivate_loan(loan_id)
    return {
        'id': loan_dict['id'],
        'student_id': loan_dict['student_id'],
        'book_id': loan_dict['book_id'],
        'loan_date': loan_dict['loan_date'].strftime('%d/%m/%Y %H:%M:%S'),
        'return_date': loan_dict['return_date'].strftime('%d/%m/%Y %H:%M:%S') if loan_dict['return_date'] else None,
        'returned': loan_dict['returned'],
        'reactivated_at': loan_dict['reactivated_at'].strftime('%d/%m/%Y %H:%M:%S')
    }
