from flask import jsonify
from api.repositories.student.student_repository import StudentRepository


def create_student(name, registration_number, class_name, grade) -> dict:
    student = StudentRepository.create(name, registration_number, class_name, grade)
    return {
        'id': student['id'],
        'name': student['name'],
        'registration_number': student['registration_number'],
        'class_name': student['class_name'],
        'grade': student['grade']
    }
