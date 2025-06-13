from flask import Flask, request
from flask_cors import CORS
import json
import os
import re

app = Flask(__name__)
CORS(app)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(root, "logs")
arquivo = os.path.join(path, "registros.json")
os.makedirs(path, exist_ok=True)

def extrair_valor_monetario(texto):
    try:
        match = re.search(r"[\d,.]+", texto.replace("R$", "").replace("r$", ""))
        if match:
            return float(match.group(0).replace(",", "."))
    except:
        pass
    return None

@app.route("/clique", methods=["POST"])
def receber_clique():
    data = request.json
    print("DADOS RECEBIDOS:", data)

    valor_aposta = extrair_valor_monetario(data.get("valorAposta", ""))
    saldo = extrair_valor_monetario(data.get("SaldoAtt", ""))

    registro = {
        "time": data.get("timeApostado", "").strip(),
        "valor_aposta": valor_aposta,
        "odd": data.get("oddSelecionada", None),
        "saldo": saldo
    }

    try:
        with open(arquivo, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
            f.flush()
    except Exception as e:
        print("Erro ao escrever no JSON:", e)

    return '', 204

if __name__ == "__main__":
    print("Servidor Flask rodando em http://localhost:5000")
    app.run(port=5000)
