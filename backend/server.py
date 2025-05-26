from flask import Flask, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(root, "logs")
arquivo = os.path.join(path, "registros.json")
os.makedirs(path, exist_ok=True)

@app.route("/clique", methods=["POST"])
def receber_clique():
    data = request.json
    print("DADOS RECEBIDOS:", data)
    try:
        with open(arquivo, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
            f.flush()
    except Exception as e:
        print("Erro ao escrever no JSON:", e)
    return '', 204

if __name__ == "__main__":
    print("Servidor Flask rodando em http://localhost:5000")
    app.run(port=5000)
