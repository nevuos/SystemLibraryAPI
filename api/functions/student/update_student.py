from flask import jsonify
from api.repositories.student.student_repository import StudentRepository


def update_student(student_id: int, name: str, registration_number: str, class_name: str, grade: str) -> dict:
    student = StudentRepository.update(
        student_id, name, registration_number, class_name, grade)
    return {
        'id': student['id'],
        'name': student['name'],
        'registration_number': student['registration_number'],
        'class_name': student['class_name'],
        'grade': student['grade']
    }
