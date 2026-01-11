from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# -----------------------
# VARIÁVEIS DE AMBIENTE
# -----------------------
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://wicbydfuhxnsudoorsjf.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpY2J5ZGZ1aHhuc3Vkb29yc2pmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgwMzE4NDYsImV4cCI6MjA4MzYwNzg0Nn0.sMmQq9t1mbAxYzkjh6To-Eo6AIWpiUvTq_t_vXMB2I")

# -----------------------
# ROTAS GET
# -----------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/chatforum")
def chat_forum():
    return render_template("chatforum.html")

@app.route("/fretes")
def fretes():
    return render_template("fretes.html")

@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

# -----------------------
# ROTA CADASTRO POST (CORRIGIDA)
# -----------------------
@app.route("/cadastro", methods=["POST"])
def cadastro_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "erro", "detalhes": "Nenhum dado recebido"}), 400

        # Validação obrigatória
        if not data.get("nome") or not data.get("senha") or not data.get("tipo"):
            return jsonify({"status": "erro", "detalhes": "Preencha nome, senha e tipo"}), 400

        # Mapeamento CORRETO dos campos frontend → backend
        dados_para_supabase = {
            "nome": data.get("nome"),
            "cpf": data.get("cpf") or None,
            "telefone": data.get("telefone") or None,
            "tipo": data.get("tipo"),
            "endereco": data.get("endereco") or None,
            "senha": data.get("senha"),
            "chave_pix": data.get("chavePix") or None  # ← CORRETO: chavePix do frontend → chave_pix do banco
        }

        # Verifique no terminal se os dados estão corretos
        print("=== DADOS RECEBIDOS DO FRONTEND ===")
        print(f"Data recebida: {data}")
        print(f"Dados para Supabase: {dados_para_supabase}")
        print("===================================")

        url = f"{SUPABASE_URL}/rest/v1/cadastro"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

        print(f"Enviando para: {url}")
        res = requests.post(url, json=dados_para_supabase, headers=headers)
        
        print(f"Resposta Supabase: {res.status_code}")
        print(f"Texto resposta: {res.text}")

        if res.status_code in (200, 201, 204):
            return jsonify({"status": "ok", "detalhes": "Cadastro realizado"})
        else:
            return jsonify({"status": "erro", "detalhes": res.text}), res.status_code

    except Exception as e:
        print(f"ERRO NO SERVIDOR: {str(e)}")
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

# -----------------------
# OUTRAS ROTAS POST (placeholders)
# -----------------------
@app.route("/login", methods=["POST"])
def login_post():
    try:
        data = request.get_json()
        return jsonify({"status": "ok", "detalhes": "Login endpoint"})
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route("/registro", methods=["POST"])
def registro_post():
    try:
        data = request.get_json()
        return jsonify({"status": "ok", "detalhes": "Registro endpoint"})
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route("/dashboard", methods=["POST"])
def dashboard_post():
    try:
        data = request.get_json()
        return jsonify({"status": "ok", "detalhes": "Dashboard endpoint"})
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route("/chatforum", methods=["POST"])
def chatforum_post():
    try:
        data = request.get_json()
        return jsonify({"status": "ok", "detalhes": "Chat forum endpoint"})
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

# -----------------------
# RODAR APP
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
