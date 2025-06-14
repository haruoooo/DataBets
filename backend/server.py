from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import re
import unicodedata
import subprocess

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

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))

@app.route("/clique", methods=["POST"])
def receber_clique():
    data = request.json
    print("DADOS RECEBIDOS:", data)

    valor_aposta = data.get("valor_aposta")
    raw_time = data.get("time")
    odd = data.get("odd") 
    time = remover_acentos(raw_time.strip()) if isinstance(raw_time, str) else raw_time
  
    registro = {
        "time": time,
        "valor_aposta": valor_aposta,
        "odd": odd
    }

    try:
        if not os.path.exists(arquivo) or os.stat(arquivo).st_size == 0:
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump([registro], f, ensure_ascii=False, indent=4)
        else:
            with open(arquivo, "r+", encoding="utf-8") as f:
                f.seek(0, os.SEEK_END)
                pos = f.tell() - 1

                while pos > 0:
                    f.seek(pos)
                    char = f.read(1)
                    if char == ']':
                        pos -= 1
                        break
                    pos -= 1

                f.seek(pos)
                f.truncate()
                f.write(',\n' + json.dumps(registro, ensure_ascii=False, indent=4) + '\n]')

        resultado = subprocess.run(["python", "backend/ml.py"], capture_output=True, text=True)
        saída = resultado.stdout.strip()
        print("[ML] Resultado ML:", saída)

        alerta = saída == "1"

    except Exception as e:
        print("[ERRO] Falha no processamento:", e)
        alerta = False  

    return jsonify({"alerta": alerta})

if __name__ == "__main__":
    print("Servidor Flask rodando em http://localhost:5000")
    app.run(port=5000)
