import os
from api.utils.update.app_operations import get_current_version


script_dir = os.path.dirname(os.path.realpath(__file__))
version_file_path = os.path.abspath(os.path.join(script_dir, '..', '..', '..', 'version.txt'))
current_version = get_current_version(version_file_path)

api_info = {
    "message": "Bem-vindo à API da Biblioteca",
    "endpoints": {
        "/books": "POST: Adicionar livro, GET: Obter todos os livros",
        "/books/<int:book_id>/deactivate": "POST: Desativar livro",
        "/books/<int:book_id>/reactivate": "POST: Reativar livro",
        "/books/search/title": "GET: Pesquisar livros por título",
        "/books/search/author": "GET: Pesquisar livros por autor",
        "/books/search/category": "GET: Pesquisar livros por categoria",
        "/books/search/barcode": "GET: Pesquisar livros por código de barras",
        "/books/<int:book_id>": "GET: Obter livro por ID, PUT: Atualizar livro",
        "/books/search/date": "GET: Pesquisar livros por intervalo de datas",
        "/books/inactive": "GET: Obter livros inativos",
        "/books/active": "GET: Obter livros ativos",
        "/books/all": "GET: Obter todos os livros",
        "/loans": "POST: Empréstimo de livro",
        "/loans/<loan_id>/return": "POST: Devolução de livro",
        "/loans/<loan_id>/deactivate": "POST: Desativar empréstimo",
        "/loans/<loan_id>/reactivate": "POST: Reativar empréstimo",
        "/loans/<loan_id>": "GET: Obter empréstimo por ID",
        "/loans/search/loan_date": "GET: Pesquisar empréstimos por intervalo de datas de empréstimo",
        "/loans/search/return_date": "GET: Pesquisar empréstimos por intervalo de datas de devolução",
        "/loans/all": "GET: Obter todos os empréstimos",
        "/loans/returned": "GET: Pesquisar empréstimos devolvidos",
        "/loans/not_returned": "GET: Pesquisar empréstimos não devolvidos",
        "/students": "POST: Adicionar estudante, GET: Obter estudantes por nome",
        "/students/<int:student_id>": "PUT: Atualizar estudante, GET: Obter estudante por ID",
        "/students/<int:student_id>/deactivate": "POST: Desativar estudante",
        "/students/<int:student_id>/reactivate": "POST: Reativar estudante",
        "/students/search/registration_number": "GET: Pesquisar estudantes por número de matrícula",
        "/students/search/class_name": "GET: Pesquisar estudantes por nome da turma",
        "/students/search/grade": "GET: Pesquisar estudantes por série",
        "/students/search/date": "GET: Pesquisar estudantes por intervalo de datas de criação",
        "/students/active": "GET: Obter estudantes ativos",
        "/students/inactive": "GET: Obter estudantes inativos",
    },
    "version": current_version,
}
