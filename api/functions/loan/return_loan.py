from ast import Dict
from api.repositories.loan.loan_repository import LoanRepository


def return_loan(loan_id) -> Dict:
    return LoanRepository.return_loan(loan_id)
