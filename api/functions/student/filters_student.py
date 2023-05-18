from api.repositories.student.student_repository import StudentRepository
from typing import List, Dict, Any


def get_students_by_field(field: str, value: str) -> List[Dict[str, Any]]:
    students = StudentRepository.get_students_by_field(field, value)
    student_list = []
    for student in students:
        student_list.append({
            'id': student['id'],
            'name': student['name'],
            'registration_number': student['registration_number'],
            'class_name': student['class_name'],
            'grade': student['grade'],
            'created_at': student['created_at'].strftime('%d/%m/%Y'),
            'deactivated_at': student['deactivated_at'].strftime('%d/%m/%Y') if student['deactivated_at'] else None,
            'status': student['status']
        })
    return student_list
