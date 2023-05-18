from api.repositories.student.student_repository import StudentRepository
from api.models.student import Student


def search_students_by_id(student_id: int) -> list:
    return StudentRepository.get_students_by_field('id', str(student_id))


def search_students_by_name(name: str, page: int = 1, per_page: int = 10) -> list:
    return StudentRepository.get_students_by_field('name', name, page=page, per_page=per_page)


def search_students_by_registration_number(registration_number: str, page: int = 1, per_page: int = 10) -> list:
    return StudentRepository.get_students_by_field('registration_number', registration_number, page=page, per_page=per_page)


def search_students_by_class_name(class_name: str, page: int = 1, per_page: int = 10) -> list:
    return StudentRepository.get_students_by_field('class_name', class_name, page=page, per_page=per_page)


def search_students_by_grade(grade: str, page: int = 1, per_page: int = 10) -> list:
    return StudentRepository.get_students_by_field('grade', grade, page=page, per_page=per_page)


def search_students_by_date_range(start_date: str, end_date: str, page: int = 1, per_page: int = 10) -> list:
    return StudentRepository.get_students_by_field('created_at', (start_date, end_date), page=page, per_page=per_page)


def get_active_students(page: int = 1, per_page: int = 10) -> list:
    return StudentRepository.get_students_by_field('status', 'active', page=page, per_page=per_page)


def get_inactive_students(page: int = 1, per_page: int = 10) -> list:
    return StudentRepository.get_students_by_field('status', 'inactive', page=page, per_page=per_page)


def get_all_students(page: int = 1, per_page: int = 10) -> dict:
    return StudentRepository.get_all_students(page=page, per_page=per_page)
