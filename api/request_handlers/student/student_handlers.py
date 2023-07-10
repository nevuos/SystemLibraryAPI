from flask import request, jsonify
from api.functions.student import (
    create_student,
    update_student,
    search_student,
    reactivate_student,
    deactivate_student
)
from api.utils.validators.generic.validate_required import validate_required_fields
from api.utils.handlers.error_handlers import handle_errors


@handle_errors
@validate_required_fields(['name', 'registration_number', 'class_name', 'grade'])
def handle_create_student_request():
    data = request.get_json()
    student = create_student(data.get('name'), data.get(
        'registration_number'), data.get('class_name'), data.get('grade'))
    return jsonify({'success': True, 'message': 'Student created successfully', 'student': student}), 200


@handle_errors
def handle_update_student_request(student_id):
    data = request.get_json()
    student = update_student(student_id, data.get('name'), data.get(
        'registration_number'), data.get('class_name'), data.get('grade'))
    return jsonify({'success': True, 'message': 'Student updated successfully', 'student': student}), 200


@handle_errors
def handle_deactivate_student_request(student_id):
    deactivate_student(student_id)
    return jsonify({'success': True, 'message': 'Student deactivated successfully'}), 200


@handle_errors
def handle_reactivate_student_request(student_id):
    reactivate_student(student_id)
    return jsonify({'success': True, 'message': 'Student reactivated successfully'}), 200


@handle_errors
def handle_get_student_by_id_request(student_id):
    student = search_student(student_id)
    return jsonify({'success': True, 'student': student}), 200


@handle_errors
def handle_search_students_by_name_request():
    name = request.args.get('name')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    students = search_student.search_students_by_name(
        name, page=page, per_page=per_page)
    return jsonify({'success': True, 'students': students}), 200


@handle_errors
def handle_search_students_by_registration_number_request():
    registration_number = request.args.get('registration_number')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    students = search_student.search_students_by_registration_number(
        registration_number, page=page, per_page=per_page)
    return jsonify({'success': True, 'students': students}), 200


@handle_errors
def handle_search_students_by_class_name_request():
    class_name = request.args.get('class_name')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    students = search_student.search_students_by_class_name(
        class_name, page=page, per_page=per_page)
    return jsonify({'success': True, 'students': students}), 200


@handle_errors
def handle_search_students_by_grade_request():
    grade = request.args.get('grade')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    students = search_student.search_students_by_grade(
        grade, page=page, per_page=per_page)
    return jsonify({'success': True, 'students': students}), 200


@handle_errors
def handle_get_active_students_request():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    students = search_student.get_active_students(page=page, per_page=per_page)
    return jsonify({'success': True, 'students': students}), 200


@handle_errors
def handle_get_inactive_students_request():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    students = search_student.get_inactive_students(page=page, per_page=per_page)
    return jsonify({'success': True, 'students': students}), 200


@handle_errors
def handle_search_students_by_date_range_request():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    students = search_student.search_students_by_date_range(
        start_date, end_date, page=page, per_page=per_page)
    return jsonify({'success': True, 'students': students}), 200


@handle_errors
def handle_get_all_students_request():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    students = search_student.get_all_students(page=page, per_page=per_page)
    return jsonify({'message': 'Students retrieved successfully', 'students': students}), 200
