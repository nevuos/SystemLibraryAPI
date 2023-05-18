from datetime import datetime
from typing import Dict, Union
from api.repositories.loan.loan_repository import LoanRepository


def create_loan(student_id, book_id) -> Dict[str, Union[int, Dict[str, str], datetime]]:
    return LoanRepository.create(student_id, book_id)
