from datetime import datetime
from api.utils.configurations.extensions import db
from api.utils.cache.cache import cache
from api.models.student import Student


class StudentNotFoundError(Exception):
    pass


class InvalidFieldError(Exception):
    pass


class StudentRepository:

    @staticmethod
    def create(name: str, registration_number: str, class_name: str, grade: str) -> dict:
        new_student = Student(
            name=name, registration_number=registration_number, class_name=class_name, grade=grade)
        db.session.add(new_student)
        db.session.commit()
        return {
            'id': new_student.id,
            'name': new_student.name,
            'registration_number': new_student.registration_number,
            'class_name': new_student.class_name,
            'grade': new_student.grade
        }

    @staticmethod
    def deactivate(student_id: int) -> dict:
        student = Student.query.get(student_id)

        if not student:
            raise StudentNotFoundError(f"No student found with id {student_id}")
        student.status = 'inactive'
        student.deactivated_at = datetime.now()
        db.session.commit()
        return {
            'deactivated_at': student.deactivated_at.strftime('%d/%m/%Y %H:%M:%S')
        }

    @staticmethod
    def reactivate(student_id: int) -> Student:
        student = Student.query.get(student_id)

        if not student:
            raise StudentNotFoundError(f"No student found with id {student_id}")
        student.status = 'active'
        student.deactivated_at = None
        db.session.commit()
        return student

    @staticmethod
    @cache.memoize(timeout=300)
    def get_students_by_field(field: str, value: str) -> list:
        if field not in ['name', 'registration_number', 'class_name', 'grade']:
            raise InvalidFieldError(f"Invalid field: {field}")

        if field == 'name':
            students = Student.query.filter(Student.name.ilike(f'%{value}%')).all()
        elif field == 'registration_number':
            students = Student.query.filter(
                Student.registration_number.ilike(f'%{value}%')).all()
        elif field == 'class_name':
            students = Student.query.filter(
                Student.class_name.ilike(f'%{value}%')).all()
        elif field == 'grade':
            students = Student.query.filter(Student.grade.ilike(f'%{value}%')).all()
        else:
            students = []

        student_list = []
        for student in students:
            student_list.append({
                'id': student.id,
                'name': student.name,
                'registration_number': student.registration_number,
                'class_name': student.class_name,
                'grade': student.grade,
                'created_at': student.created_at.strftime('%d/%m/%Y'),
                'deactivated_at': student.deactivated_at.strftime('%d/%m/%Y') if student.deactivated_at else None,
                'status': student.status
            })
        return student_list

    @staticmethod
    @cache.memoize(timeout=300)
    def get_all_students(page: int = 1, per_page: int = 10) -> dict:
        pagination = Student.query.paginate(page=page, per_page=per_page)
        students = pagination.items

        student_list = [{
            'id': student.id,
            'name': student.name,
            'registration_number': student.registration_number,
            'class_name': student.class_name,
            'grade': student.grade,
            'created_at': student.created_at.strftime('%d/%m/%Y'),
            'status': student.status
        } for student in students]

        return {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'items': student_list
        }

    @staticmethod
    def update(student_id: int, name: str = "", registration_number: str = "",
               class_name: str = "", grade: str = "") -> dict:
        student = Student.query.get(student_id)

        if not student:
            raise StudentNotFoundError(f"No student found with id {student_id}")

        if name:
            student.name = name
        if registration_number:
            student.registration_number = registration_number
        if class_name:
            student.class_name = class_name
        if grade:
            student.grade = grade

        db.session.commit()

        return {
            'id': student.id,
            'name': student.name,
            'registration_number': student.registration_number,
            'class_name': student.class_name,
            'grade': student.grade
        }
