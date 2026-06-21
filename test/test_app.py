import pytest
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

ARQUIVO_TESTE = 'tarefas_teste.json'

@pytest.fixture
def client():
    app.config['TESTING'] = True

    tarefas_iniciais = [
        {"id": 1, "titulo": "Tarefa Teste", "concluida": False}
    ]

    with open(ARQUIVO_TESTE, 'w', encoding='utf-8') as f:
        json.dump(tarefas_iniciais, f)

    with app.test_client() as client:
        yield client

    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)

def test_listar_tarefas(client):
    response = client.get('/tarefas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_criar_tarefa(client):
    response = client.post('/tarefas',
        data=json.dumps({"titulo": "Nova Tarefa"}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["titulo"] == "Nova Tarefa"
    assert data["concluida"] == False

def test_criar_tarefa_sem_titulo(client):
    response = client.post('/tarefas',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "erro" in data

def test_criar_tarefa_titulo_vazio(client):
    response = client.post('/tarefas',
        data=json.dumps({"titulo": "   "}),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_deletar_tarefa_inexistente(client):
    response = client.delete('/tarefas/999')
    assert response.status_code in [400, 404]
    data = json.loads(response.data)
    assert "erro" in data