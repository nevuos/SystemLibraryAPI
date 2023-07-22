from flask import Blueprint, request
from api.utils.configurations.extensions import limiter
from api.functions.loan import (
    create_loan,
    return_loan,
    deactivate_loan,
    reactivate_loan,
    search_loan
)

loan_bp = Blueprint('loan_routes', __name__)


@loan_bp.route('/loans', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_create_loan_request():
    data = request.get_json()
    return create_loan(data.get('student_id'), data.get('book_id'))


@loan_bp.route('/loans/<loan_id>/return', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_return_loan_request(loan_id):
    return return_loan(loan_id)


@loan_bp.route('/loans/<loan_id>/deactivate', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_deactivate_loan_request(loan_id):
    return deactivate_loan(loan_id)


@loan_bp.route('/loans/<loan_id>/reactivate', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_reactivate_loan_request(loan_id):
    return reactivate_loan(loan_id)


@loan_bp.route('/loans/<loan_id>', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_get_loan_by_id_request(loan_id):
    return search_loan.get_loan_by_id(loan_id)


@loan_bp.route('/loans', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_search_loans_by_student_id_request():
    student_id = request.args.get('student_id')
    return search_loan.search_loans_by_student_id(student_id)


@loan_bp.route('/loans', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_search_loans_by_book_id_request():
    book_id = request.args.get('book_id')
    return search_loan.search_loans_by_book_id(book_id)


@loan_bp.route('/loans/search/loan_date', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_search_loans_by_loan_date_range_request():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return search_loan.search_loans_by_loan_date_range(start_date, end_date)


@loan_bp.route('/loans/search/return_date', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_search_loans_by_return_date_range_request():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return search_loan.search_loans_by_return_date_range(start_date, end_date)


@loan_bp.route('/loans/all', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_get_all_loans_request():
    return search_loan.get_all_loans()


@loan_bp.route('/loans/returned', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_search_loans_returned_request():
    return search_loan.search_loans_returned()


@loan_bp.route('/loans/not_returned', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_search_loans_not_returned_request():
    return search_loan.search_loans_not_returned()
