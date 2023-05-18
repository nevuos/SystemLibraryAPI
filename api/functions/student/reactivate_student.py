from api.repositories.student.student_repository import StudentRepository
from api.models.student import Student


def reactivate_student(student_id: int) -> Student:
    return StudentRepository.reactivate(student_id)
