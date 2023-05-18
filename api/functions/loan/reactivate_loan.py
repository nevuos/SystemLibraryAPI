from typing import Dict, Any
from api.repositories.loan.loan_repository import LoanRepository


def reactivate_loan(loan_id) -> Dict[str, Any]:
    loan = LoanRepository.reactivate_loan(loan_id)
    return {
        'id': loan.id,
        'student_id': loan.student_id,
        'book_id': loan.book_id,
        'loan_date': loan.loan_date.strftime('%d/%m/%Y %H:%M:%S'),
        'return_date': loan.return_date.strftime('%d/%m/%Y %H:%M:%S') if loan.return_date else None,
        'returned': loan.returned,
    }
