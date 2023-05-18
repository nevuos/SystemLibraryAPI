from flask import request, jsonify
from api.functions.loan import (
    create_loan,
    return_loan,
    deactivate_loan,
    reactivate_loan,
    search_loan
)
from api.utils.validators.generic.validate_required import validate_required_fields
from api.request_handlers.errors.error_handlers import handle_errors


@handle_errors
@validate_required_fields(['student_id', 'book_id'])
def handle_create_loan_request():
    data = request.get_json()
    loan = create_loan(data.get('student_id'), data.get('book_id'))
    return jsonify({'message': 'Loan created successfully', 'loan': loan}), 200


@handle_errors
def handle_return_loan_request(loan_id):
    loan = return_loan(loan_id)
    return jsonify({'message': 'Loan returned successfully', 'loan': loan}), 200


@handle_errors
def handle_deactivate_loan_request(loan_id):
    loan = deactivate_loan(loan_id)
    return jsonify({'message': 'Loan deactivated successfully', 'loan': loan}), 200


@handle_errors
def handle_reactivate_loan_request(loan_id):
    loan = reactivate_loan(loan_id)
    return jsonify({'message': 'Loan reactivated successfully', 'loan': loan}), 200


@handle_errors
def handle_get_loan_by_id_request(loan_id):
    loan = search_loan.get_loan_by_id(loan_id)
    return jsonify({'message': 'Loan retrieved successfully', 'loan': loan}), 200


@handle_errors
def handle_search_loans_by_student_id_request():
    student_id = request.args.get('student_id')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    loans = search_loan.search_loans_by_student_id(
        student_id, page=page, per_page=per_page)
    return jsonify({'message': 'Loans retrieved successfully', 'loans': loans}), 200


@handle_errors
def handle_search_loans_by_book_id_request():
    book_id = request.args.get('book_id')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    loans = search_loan.search_loans_by_book_id(book_id, page=page, per_page=per_page)
    return jsonify({'message': 'Loans retrieved successfully', 'loans': loans}), 200


@handle_errors
def handle_search_loans_by_loan_date_range_request():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    loans = search_loan.search_loans_by_loan_date_range(
        start_date, end_date, page=page, per_page=per_page)
    return jsonify({'message': 'Loans retrieved successfully', 'loans': loans}), 200


@handle_errors
def handle_search_loans_by_return_date_range_request():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    loans = search_loan.search_loans_by_return_date_range(
        start_date, end_date, page=page, per_page=per_page)
    return jsonify({'message': 'Loans retrieved successfully', 'loans': loans}), 200


@handle_errors
def handle_get_all_loans_request():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    loans = search_loan.get_all_loans(page=page, per_page=per_page)
    return jsonify({'message': 'Loans retrieved successfully', 'loans': loans}), 200


@handle_errors
def handle_search_loans_returned_request():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    loans = search_loan.search_loans_returned(page=page, per_page=per_page)
    return jsonify({'message': 'Returned loans retrieved successfully', 'loans': loans}), 200


@handle_errors
def handle_search_loans_not_returned_request():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    loans = search_loan.search_loans_not_returned(page=page, per_page=per_page)
    return jsonify({'message': 'Not returned loans retrieved successfully', 'loans': loans}), 200
