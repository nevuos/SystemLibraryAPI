# API de Biblioteca

Bem-vindo à API de Biblioteca! Esta API foi desenvolvida para gerenciar um sistema de biblioteca. Ela fornece endpoints para realizar operações relacionadas a livros, empréstimos e estudantes.

## Recursos da API

### Livros

- **Adicionar livro:**
  - `POST /books`: Adiciona um novo livro ao sistema.

- **Obter livros:**
  - `GET /books`: Retorna todos os livros cadastrados no sistema.
  - `GET /books/<int:book_id>`: Retorna informações de um livro específico com base no ID.

- **Atualizar livro:**
  - `PUT /books/<int:book_id>`: Atualiza as informações de um livro específico com base no ID.

- **Desativar/Reativar livro:**
  - `POST /books/<int:book_id>/deactivate`: Desativa um livro específico com base no ID.
  - `POST /books/<int:book_id>/reactivate`: Reativa um livro específico com base no ID.

- **Pesquisar livros:**
  - `GET /books/search/title?query=<titulo>`: Pesquisa livros por título.
  - `GET /books/search/author?query=<autor>`: Pesquisa livros por autor.
  - `GET /books/search/category?query=<categoria>`: Pesquisa livros por categoria.
  - `GET /books/search/barcode?query=<codigo_barras>`: Pesquisa livros por código de barras.
  - `GET /books/search/date?start_date=<data_inicial>&end_date=<data_final>`: Pesquisa livros por intervalo de datas.

### Empréstimos

- **Realizar empréstimo/devolução:**
  - `POST /loans`: Realiza um novo empréstimo de livro.
  - `POST /loans/<loan_id>/return`: Registra a devolução de um livro emprestado.

- **Obter empréstimos:**
  - `GET /loans`: Retorna todos os empréstimos cadastrados no sistema.
  - `GET /loans/<loan_id>`: Retorna informações de um empréstimo específico com base no ID.

- **Desativar/Reativar empréstimo:**
  - `POST /loans/<loan_id>/deactivate`: Desativa um empréstimo específico com base no ID.
  - `POST /loans/<loan_id>/reactivate`: Reativa um empréstimo específico com base no ID.

- **Pesquisar empréstimos:**
  - `GET /loans/search/loan_date?start_date=<data_inicial>&end_date=<data_final>`: Pesquisa empréstimos por intervalo de datas de empréstimo.
  - `GET /loans/search/return_date?start_date=<data_inicial>&end_date=<data_final>`: Pesquisa empréstimos por intervalo de datas de devolução.

### Estudantes

- **Adicionar estudante:**
  - `POST /students`: Adiciona um novo estudante ao sistema.

- **Obter estudantes:**
  - `GET /students`: Retorna todos os estudantes cadastrados no sistema.
  - `GET /students/<int:student_id>`: Retorna informações de um estudante específico com base no ID.

- **Atualizar estudante:**
  - `PUT /students/<int:student_id>`: Atualiza as informações de um estudante específico com base no ID.

- **Desativar/Reativar estudante:**
  - `POST /students/<int:student_id>/deactivate`: Desativa um estudante específico com base no ID.
  - `POST /students/<int:student_id>/reactivate`: Reativa um estudante específico com base no ID.

- **Pesquisar estudantes:**
  - `GET /students/search/registration_number?query=<numero_matricula>`: Pesquisa estudantes por número de matrícula.
  - `GET /students/search/class_name?query=<nome_turma>`: Pesquisa estudantes por nome da turma.
  - `GET /students/search/grade?query=<serie>`: Pesquisa estudantes por série.
  - `GET /students/search/date?start_date=<data_inicial>&end_date=<data_final>`: Pesquisa estudantes por intervalo de datas de criação.

## Autenticação e Autorização

A API de Biblioteca é protegida por autenticação baseada em token. Para acessar os endpoints, é necessário obter um token de acesso. Para isso, faça uma solicitação POST para `/auth/login` com as credenciais de usuário para receber o token.

O token deve ser incluído no cabeçalho `Authorization` de todas as solicitações autenticadas no formato `Bearer <token>`. Caso contrário, as solicitações serão recusadas com status 401 (Não autorizado).

## Executando Localmente

Para executar a API localmente, siga as etapas abaixo:

1. Certifique-se de ter o Python 3.x e o pip instalados em sua máquina.

2. Clone este repositório em sua máquina local:

   ```shell
   git clone https://github.com/seu-usuario/seu-repositorio.git

3. Navegue até o diretório do projeto:

   ```shell
   cd seu-repositorio
   
4. Instale as dependências necessárias:
  
   ```shell
   pip install -r requirements.txt
    
5. Execute a aplicação:
    
   ```shell
   python run.py 
   
6. A API estará disponível em:

    ```shell
    http://localhost:5000.


## Contribuindo

Se você encontrar algum problema ou tiver alguma sugestão de melhoria, sinta-se à vontade para abrir uma [issue](https://github.com/nevuos/systemLibraryAPI/issues) ou enviar um [pull request](https://github.com/nevuos/systemLibraryAPI/pulls).
