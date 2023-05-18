from api.repositories.student.student_repository import StudentRepository


def deactivate_student(student_id) -> dict:
    return StudentRepository.deactivate(student_id)
