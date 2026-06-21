# API de Tarefas — Flask

API REST construída com Flask para gerenciar tarefas (To-Do List), desenvolvida em sprints semanais como projeto de portfólio.

---

## Tecnologias usadas

- Python 3.x
- Flask
- Pytest

---

## Instalação

```bash
pip install flask pytest
```

---

## Estrutura do projeto
api-tarefas-flask/

├── test/

│   ├── init.py

│   └── test_app.py        ← testes automatizados

├── app.py                 ← API Flask com todas as rotas

├── tarefas.json           ← banco de dados em JSON

├── .gitignore

├── requirements.txt

└── README.md

---

## Como rodar

```bash
python app.py
```

Servidor em: `http://127.0.0.1:5000`

---

## Endpoints

### GET /tarefas
Lista todas as tarefas.

### POST /tarefas
Cria uma nova tarefa.
```json
{ "titulo": "Minha nova tarefa" }
```

### PUT /tarefas/{id}
Atualiza uma tarefa existente.
```json
{ "titulo": "Título atualizado", "concluida": true }
```

### DELETE /tarefas/{id}
Apaga uma tarefa.

---

## Códigos de resposta

| Código | Significado |
|--------|-------------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 405 | Method Not Allowed |

---

## Como rodar os testes

```bash
python -m pytest test/
```

Resultado esperado:
collected 5 items

test\test_app.py .....

5 passed

---

## Validações

- `titulo` é obrigatório no POST
- `titulo` não pode ser vazio ou só espaços
- Body deve ser JSON válido
- Retorna erro claro quando tarefa não encontrada
