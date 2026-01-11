from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Variáveis de ambiente do Vercel
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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

# -----------------------
# ROTA POST DO CADASTRO COM TODOS OS CAMPOS
# -----------------------
@app.route("/cadastro", methods=["POST"])
def cadastro_post():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"status": "erro", "detalhes": "Nenhum dado recebido"}), 400
        
        # GARANTE TODOS OS CAMPOS DA TABELA
        campos_completos = {
            "nome": data.get("nome", ""),
            "cpf": data.get("cpf", ""),
            "telefone": data.get("telefone", ""),
            "tipo": data.get("tipo", ""),
            "endereco": data.get("endereco", ""),
            "senha": data.get("senha", ""),
            "chave_pix": data.get("chave_pix", "")
            # id e created_at são gerados automaticamente
        }
        
        # Campos obrigatórios
        if not campos_completos["nome"] or not campos_completos["senha"] or not campos_completos["tipo"]:
            return jsonify({"status": "erro", "detalhes": "Preencha nome, senha e tipo"}), 400
        
        url = f"{SUPABASE_URL}/rest/v1/cadastro"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        res = requests.post(url, json=campos_completos, headers=headers)
        
        if res.status_code in (200, 201, 204):
            return jsonify({"status": "ok", "detalhes": "Cadastro realizado"})
        else:
            return jsonify({"status": "erro", "detalhes": res.text}), res.status_code
            
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

# -----------------------
# ROTAS POST PARA OUTROS TEMPLATES
# -----------------------
@app.route("/login", methods=["POST"])
def login_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "erro", "detalhes": "Nenhum dado"}), 400
        
        # Aqui você implementaria a lógica de login
        return jsonify({"status": "ok", "detalhes": "Login endpoint"})
        
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route("/registro", methods=["POST"])
def registro_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "erro", "detalhes": "Nenhum dado"}), 400
        
        # Lógica para registro
        return jsonify({"status": "ok", "detalhes": "Registro endpoint"})
        
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route("/dashboard", methods=["POST"])
def dashboard_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "erro", "detalhes": "Nenhum dado"}), 400
        
        # Lógica para dashboard
        return jsonify({"status": "ok", "detalhes": "Dashboard endpoint"})
        
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route("/chatforum", methods=["POST"])
def chatforum_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "erro", "detalhes": "Nenhum dado"}), 400
        
        # Lógica para chat/forum
        return jsonify({"status": "ok", "detalhes": "Chat forum endpoint"})
        
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
