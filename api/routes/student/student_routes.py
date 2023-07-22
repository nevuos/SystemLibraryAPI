from flask import Blueprint, request
from api.utils.configurations.extensions import limiter
from api.request_handlers.student.student_handlers import (
    handle_create_student_request,
    handle_get_all_students_request,
    handle_search_students_by_date_range_request,
    handle_update_student_request,
    handle_get_student_by_id_request,
    handle_search_students_by_name_request,
    handle_deactivate_student_request,
    handle_reactivate_student_request,
    handle_search_students_by_registration_number_request,
    handle_search_students_by_class_name_request,
    handle_search_students_by_grade_request,
    handle_get_active_students_request,
    handle_get_inactive_students_request,
)


student_bp = Blueprint('student_routes', __name__)


@student_bp.route('/students', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def add_student_route():
    return handle_create_student_request()


@student_bp.route('/students/<int:student_id>', methods=['PUT'])
@limiter.limit("1000/day;100/hour;30/minute")
def update_student_route(student_id):
    return handle_update_student_request(student_id)


@student_bp.route('/students/<int:student_id>', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def get_student_by_id_route(student_id):
    return handle_get_student_by_id_request(student_id)


@student_bp.route('/students', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def get_students_by_name_route():
    return handle_search_students_by_name_request()


@student_bp.route('/students/<int:student_id>/deactivate', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def deactivate_student_route(student_id):
    return handle_deactivate_student_request(student_id)


@student_bp.route('/students/<int:student_id>/reactivate', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def reactivate_student_route(student_id):
    return handle_reactivate_student_request(student_id)


@student_bp.route('/students/search/registration_number', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def get_students_by_registration_number_route():
    return handle_search_students_by_registration_number_request()


@student_bp.route('/students/search/class_name', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def get_students_by_class_name_route():
    return handle_search_students_by_class_name_request()


@student_bp.route('/students/search/grade', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def get_students_by_grade_route():
    return handle_search_students_by_grade_request()


@student_bp.route('/students/search/date', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def search_students_by_date_range_route():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return handle_search_students_by_date_range_request(start_date, end_date)


@student_bp.route('/students/active', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def get_active_students_route():
    return handle_get_active_students_request()


@student_bp.route('/students/inactive', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def get_inactive_students_route():
    return handle_get_inactive_students_request()


@student_bp.route('/students/all', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def get_all_students_route():
    return handle_get_all_students_request()
