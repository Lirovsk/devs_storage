# flask_DIO

Complete documentation for the Flask API in this repository.

============================================================

## ENGLISH DOCUMENTATION

============================================================

1. Overview

This project exposes a REST API built with Flask to manage:

- users
- habilities (skills) linked to users

Data is stored in a local SQLite database file:

- teste.db

Core technologies:

- Flask (HTTP API)
- SQLAlchemy (ORM + database access)
- SQLite (database engine)

1. Project Structure

- main.py
 Starts the Flask app and defines HTTP routes.

- DBworks/models.py
 Defines SQLAlchemy models:
  - user
  - hability

- DBworks/sql_services.py
 Implements low-level database operations (create/search/delete).

- DBworks/services.py
 Implements business rules and JSON responses used by the routes.

1. Data Model

User (table: users)

- id: integer, primary key
- name: string
- age: integer
- email: string
- super_user: boolean (default: false)
- habilities: one-to-many relation with hability

Hability (table: habilities)

- id: integer, primary key
- name: string
- level: integer
- description: string or null
- user_id: foreign key to users.id

1. How The API Works (Request Flow)

1. Client sends an HTTP request to one of the Flask routes in main.py.
1. Route reads path parameters and/or JSON body.
1. Route calls a function from DBworks/services.py.
1. Service applies business validations (for example: check if user exists).
1. Service calls DBworks/sql_services.py for database access.
1. Service returns a JSON string with:

- status (0 = success, 1 = error)
- message
- optional data object

1. Route returns that JSON string as HTTP response body.

1. Running The API

Requirements:

- Python 3.10+
- Flask
- SQLAlchemy

Install dependencies:

- pip install flask sqlalchemy

Run application:

- python main.py

Default local URL:

- <http://127.0.0.1:5000>

1. API Endpoints

Important:

- Route names use the word hability (same spelling as source code).
- Request/response examples below are JSON.

6.1 Insert User

Method and route:

- POST /insert_user/

Body:

- {
  "name": "Alice",
  "age": 27,
  "email": "<alice@example.com>"
 }

Success response:

- {
  "status": 0,
  "message": "User Alice created successfully!"
 }

Error response (already exists):

- {
  "status": 1,
  "message": "User with the same name or email already exists."
 }

6.2 Search User By Name

Method and route:

- GET /search_user_by_name/<name>

Example:

- GET /search_user_by_name/Alice

Success response:

- {
  "status": 0,
  "message": "User Alice found!",
  "user_data": {
   "name": "Alice",
   "age": 27,
   "email": "<alice@example.com>"
  }
 }

Not found response:

- {
  "status": 1,
  "message": "User not found."
 }

6.3 Search User By Email

Method and route:

- GET /search_user_by_email/<email>

Example:

- GET /search_user_by_email/alice@example.com

Success response:

- {
  "status": 0,
  "message": "User Alice found!",
  "user_data": {
   "name": "Alice",
   "age": 27,
   "email": "<alice@example.com>"
  }
 }

Not found response:

- {
  "status": 1,
  "message": "User not found."
 }

6.4 Delete User

Method and route:

- DELETE /delete_user/<email>

Example:

- DELETE /delete_user/alice@example.com

Success response:

- {
  "status": 0,
  "message": "User Alice deleted successfully!"
 }

Not found response:

- {
  "status": 1,
  "message": "User not found."
 }

6.5 Create Hability

Method and route:

- POST /create_hability/

Body:

- {
  "hability_name": "python",
  "hability_level": 3,
  "user_email": "<alice@example.com>",
  "hability_description": "Backend automation"
 }

Business rules:

- User must exist.
- Hability name is treated in lowercase in storage/search.
- If hability_level is greater than 4, it is limited to 4.
- Duplicate hability for the same user is not allowed.

Success response:

- {
  "status": 0,
  "message": "Hability python created successfully for user Alice!"
 }

Error response (user not found):

- {
  "status": 1,
  "message": "User not found."
 }

Error response (already exists):

- {
  "status": 1,
  "message": "Hability with the name python already exists for this user."
 }

6.6 Search Hability By Name

Method and route:

- GET /search_hability_by_name/<hability_name>/<user_email>

Example:

- GET /search_hability_by_name/python/alice@example.com

Success response:

- {
  "status": 0,
  "message": "Hability Python found for user Alice!",
  "hability_data": {
   "name": "Python",
   "level": 3,
   "description": "Backend automation"
  }
 }

Error response:

- {
  "status": 1,
  "message": "Hability python not found for user Alice."
 }

6.7 Delete Hability

Method and route:

- DELETE /delete_hability/<hability_name>/<user_email>

Example:

- DELETE /delete_hability/python/alice@example.com

Success response:

- {
  "status": 0,
  "message": "Hability Python deleted successfully for user Alice!"
 }

Error response:

- {
  "status": 1,
  "message": "Hability python not found for user Alice."
 }

1. Status Convention

All service responses use:

- status = 0 -> success
- status = 1 -> error

1. Notes And Limitations

- Responses are returned as JSON text generated with json.dumps.
- HTTP status codes are not customized (default is usually 200 unless Flask errors occur).
- Database is local SQLite; for production usage, add security, migrations, validations, and better error handling.

1. Quick Test With curl

Create user:

- curl -X POST <http://127.0.0.1:5000/insert_user/> -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"age\":27,\"email\":\"<alice@example.com>\"}"

Create hability:

- curl -X POST <http://127.0.0.1:5000/create_hability/> -H "Content-Type: application/json" -d "{\"hability_name\":\"python\",\"hability_level\":3,\"user_email\":\"<alice@example.com>\",\"hability_description\":\"Backend automation\"}"

Search user by email:

- curl <http://127.0.0.1:5000/search_user_by_email/alice@example.com>

============================================================

## DOCUMENTACAO EM PORTUGUES

============================================================

1. Visao Geral

Este projeto expoe uma API REST feita com Flask para gerenciar:

- usuarios
- habilities (habilidades) vinculadas aos usuarios

Os dados sao armazenados em um banco SQLite local:

- teste.db

Tecnologias principais:

- Flask (API HTTP)
- SQLAlchemy (ORM + acesso ao banco)
- SQLite (motor do banco)

1. Estrutura Do Projeto

- main.py
 Inicia a aplicacao Flask e define as rotas HTTP.

- DBworks/models.py
 Define os modelos SQLAlchemy:
  - user
  - hability

- DBworks/sql_services.py
 Implementa as operacoes de baixo nivel no banco (criar/buscar/deletar).

- DBworks/services.py
 Implementa regras de negocio e respostas JSON usadas pelas rotas.

1. Modelo De Dados

User (tabela: users)

- id: inteiro, chave primaria
- name: texto
- age: inteiro
- email: texto
- super_user: booleano (padrao: false)
- habilities: relacao um-para-muitos com hability

Hability (tabela: habilities)

- id: inteiro, chave primaria
- name: texto
- level: inteiro
- description: texto ou nulo
- user_id: chave estrangeira para users.id

1. Como A API Funciona (Fluxo)

1. O cliente envia uma requisicao HTTP para uma rota em main.py.
1. A rota le parametros de caminho e/ou corpo JSON.
1. A rota chama uma funcao em DBworks/services.py.
1. O service aplica validacoes de negocio (exemplo: usuario existe).
1. O service chama DBworks/sql_services.py para acessar o banco.
1. O service retorna uma string JSON com:

- status (0 = sucesso, 1 = erro)
- message
- objeto de dados opcional

1. A rota devolve essa string JSON como corpo da resposta HTTP.

1. Executando A API

Requisitos:

- Python 3.10+
- Flask
- SQLAlchemy

Instalar dependencias:

- pip install flask sqlalchemy

Executar aplicacao:

- python main.py

URL local padrao:

- <http://127.0.0.1:5000>

1. Endpoints Da API

Importante:

- Os nomes das rotas usam hability (mesma grafia do codigo).
- Os exemplos de requisicao/resposta abaixo estao em JSON.

6.1 Inserir Usuario

Metodo e rota:

- POST /insert_user/

Body:

- {
  "name": "Alice",
  "age": 27,
  "email": "<alice@example.com>"
 }

Resposta de sucesso:

- {
  "status": 0,
  "message": "User Alice created successfully!"
 }

Resposta de erro (ja existe):

- {
  "status": 1,
  "message": "User with the same name or email already exists."
 }

6.2 Buscar Usuario Por Nome

Metodo e rota:

- GET /search_user_by_name/<name>

Exemplo:

- GET /search_user_by_name/Alice

Resposta de sucesso:

- {
  "status": 0,
  "message": "User Alice found!",
  "user_data": {
   "name": "Alice",
   "age": 27,
   "email": "<alice@example.com>"
  }
 }

Resposta quando nao encontrado:

- {
  "status": 1,
  "message": "User not found."
 }

6.3 Buscar Usuario Por Email

Metodo e rota:

- GET /search_user_by_email/<email>

Exemplo:

- GET /search_user_by_email/alice@example.com

Resposta de sucesso:

- {
  "status": 0,
  "message": "User Alice found!",
  "user_data": {
   "name": "Alice",
   "age": 27,
   "email": "<alice@example.com>"
  }
 }

Resposta quando nao encontrado:

- {
  "status": 1,
  "message": "User not found."
 }

6.4 Deletar Usuario

Metodo e rota:

- DELETE /delete_user/<email>

Exemplo:

- DELETE /delete_user/alice@example.com

Resposta de sucesso:

- {
  "status": 0,
  "message": "User Alice deleted successfully!"
 }

Resposta quando nao encontrado:

- {
  "status": 1,
  "message": "User not found."
 }

6.5 Criar Hability

Metodo e rota:

- POST /create_hability/

Body:

- {
  "hability_name": "python",
  "hability_level": 3,
  "user_email": "<alice@example.com>",
  "hability_description": "Backend automation"
 }

Regras de negocio:

- O usuario precisa existir.
- O nome da hability e tratado em minusculas para salvar/buscar.
- Se hability_level for maior que 4, o valor e limitado para 4.
- Nao permite hability duplicada para o mesmo usuario.

Resposta de sucesso:

- {
  "status": 0,
  "message": "Hability python created successfully for user Alice!"
 }

Resposta de erro (usuario nao encontrado):

- {
  "status": 1,
  "message": "User not found."
 }

Resposta de erro (ja existe):

- {
  "status": 1,
  "message": "Hability with the name python already exists for this user."
 }

6.6 Buscar Hability Por Nome

Metodo e rota:

- GET /search_hability_by_name/<hability_name>/<user_email>

Exemplo:

- GET /search_hability_by_name/python/alice@example.com

Resposta de sucesso:

- {
  "status": 0,
  "message": "Hability Python found for user Alice!",
  "hability_data": {
   "name": "Python",
   "level": 3,
   "description": "Backend automation"
  }
 }

Resposta de erro:

- {
  "status": 1,
  "message": "Hability python not found for user Alice."
 }

6.7 Deletar Hability

Metodo e rota:

- DELETE /delete_hability/<hability_name>/<user_email>

Exemplo:

- DELETE /delete_hability/python/alice@example.com

Resposta de sucesso:

- {
  "status": 0,
  "message": "Hability Python deleted successfully for user Alice!"
 }

Resposta de erro:

- {
  "status": 1,
  "message": "Hability python not found for user Alice."
 }

1. Convencao De Status

Todas as respostas dos services usam:

- status = 0 -> sucesso
- status = 1 -> erro

1. Observacoes E Limitacoes

- As respostas sao retornadas como texto JSON gerado por json.dumps.
- Os codigos HTTP nao sao personalizados (em geral retorna 200, exceto erros internos do Flask).
- O banco e SQLite local; para producao, adicione seguranca, migracoes, validacoes e tratamento de erro mais robusto.

1. Teste Rapido Com curl

Criar usuario:

- curl -X POST <http://127.0.0.1:5000/insert_user/> -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"age\":27,\"email\":\"<alice@example.com>\"}"

Criar hability:

- curl -X POST <http://127.0.0.1:5000/create_hability/> -H "Content-Type: application/json" -d "{\"hability_name\":\"python\",\"hability_level\":3,\"user_email\":\"<alice@example.com>\",\"hability_description\":\"Backend automation\"}"

Buscar usuario por email:

- curl <http://127.0.0.1:5000/search_user_by_email/alice@example.com>
