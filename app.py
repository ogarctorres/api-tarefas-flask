from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

ARQUIVO = 'tarefas.json'

def ler_tarefas():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_tarefas(tarefas):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)

# GET — listar todas as tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    return jsonify(ler_tarefas())

# POST — criar nova tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Body da requisição inválido ou vazio"}), 400

    if "titulo" not in dados:
        return jsonify({"erro": "Campo 'titulo' é obrigatório"}), 400

    if not dados["titulo"].strip():
        return jsonify({"erro": "Campo 'titulo' não pode ser vazio"}), 400
    
    tarefas = ler_tarefas()
    
    nova_tarefa = {
        "id": max([t["id"] for t in tarefas], default=0) + 1,
        "titulo": dados["titulo"],
        "concluida": False
    }
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    return jsonify(nova_tarefa), 201

# PUT — atualizar tarefa existente
# PUT — atualizar tarefa existente
@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Body da requisição inválido ou vazio"}), 400

    tarefas = ler_tarefas()
    for tarefa in tarefas:
        if tarefa["id"] == id:
            if "titulo" in dados and not dados["titulo"].strip():
                return jsonify({"erro": "Campo 'titulo' não pode ser vazio"}), 400
            tarefa["titulo"] = dados.get("titulo", tarefa["titulo"]).strip()
            tarefa["concluida"] = dados.get("concluida", tarefa["concluida"])
            salvar_tarefas(tarefas)
            return jsonify(tarefa)

    return jsonify({"erro": f"Tarefa com id {id} não encontrada"}), 404

# DELETE — apagar tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    tarefas = ler_tarefas()
    for i, tarefa in enumerate(tarefas):
        if tarefa["id"] == id:
            tarefas.pop(i)
            salvar_tarefas(tarefas)
            return jsonify({"mensagem": "Tarefa deletada"})
    return jsonify({"erro": "Tarefa não encontrada"}), 404

@app.errorhandler(404)
def nao_encontrado(e):
    return jsonify({"erro": "Rota não encontrada"}), 404

@app.errorhandler(405)
def metodo_nao_permitido(e):
    return jsonify({"erro": "Método não permitido"}), 405

if __name__ == '__main__':
    app.run(debug=True)