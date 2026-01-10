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
# ROTA POST DO CADASTRO
# -----------------------
@app.route("/cadastro", methods=["POST"])
def cadastro_post():
    data = request.json

    if not data:
        return jsonify({"status": "erro", "detalhes": "Nenhum dado recebido"}), 400

    url = f"{SUPABASE_URL}/rest/v1/cadastro"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    try:
        res = requests.post(url, json=data, headers=headers)
        if res.status_code in [200, 201, 204]:
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "erro", "detalhes": res.text}), res.status_code
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500


if __name__ == "__main__":
    # debug=True só para desenvolvimento, em produção use False
    app.run(debug=True)
