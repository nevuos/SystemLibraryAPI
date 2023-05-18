from typing import Dict, Any
from api.repositories.loan.loan_repository import LoanRepository


def deactivate_loan(loan_id) -> Dict[str, Any]:
    result = LoanRepository.deactivate_loan(loan_id)
    response = {
        'message': result['message'],
        'deactivated_at': result['deactivated_at']
    }
    return response
