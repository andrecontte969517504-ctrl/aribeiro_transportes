from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

# Configuração do Supabase - use variáveis de ambiente ou valores diretos
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://wicbydfuhxnsudoorsjf.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpY2J5ZGZ1aHhuc3Vkb29yc2pmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgwMzE4NDYsImV4cCI6MjA4MzYwNzg0Nn0.sMmQq9t1mbAxYzkjh6To-Eo6AIWpiUvTq_t_vXMB2I")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=["POST"])
def cadastro_post():
    try:
        data = request.json
        
        # Validação dos campos obrigatórios
        if not data.get('nome'):
            return jsonify({"status": "erro", "detalhes": "Nome é obrigatório"}), 400
        
        if not data.get('senha'):
            return jsonify({"status": "erro", "detalhes": "Senha é obrigatória"}), 400
        
        if not data.get('tipo'):
            return jsonify({"status": "erro", "detalhes": "Tipo de usuário é obrigatório"}), 400
        
        # Validação do tipo
        tipos_permitidos = ['gerente', 'motorista', 'ajudante', 'cliente']
        if data.get('tipo') not in tipos_permitidos:
            return jsonify({"status": "erro", "detalhes": f"Tipo inválido. Deve ser um dos: {', '.join(tipos_permitidos)}"}), 400
        
        # Preparar dados para o Supabase
        supabase_data = {
            "nome": data['nome'],
            "cpf": data.get('cpf'),
            "telefone": data.get('telefone'),
            "tipo": data['tipo'],
            "endereco": data.get('endereco'),
            "senha": data['senha'],
            "chave_pix": data.get('chave_pix')
        }
        
        # Remover campos nulos (opcional)
        supabase_data = {k: v for k, v in supabase_data.items() if v is not None}
        
        url = f"{SUPABASE_URL}/rest/v1/cadastro"
        
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        # Fazer requisição para o Supabase
        res = requests.post(url, json=supabase_data, headers=headers, timeout=10)
        
        print(f"Status Code Supabase: {res.status_code}")
        print(f"Resposta Supabase: {res.text}")
        
        if res.status_code in [200, 201, 204]:
            # Criar resposta com cookie
            response = jsonify({
                "status": "ok", 
                "message": "Cadastro realizado com sucesso!",
                "id": res.json()[0]['id'] if res.text and res.text.strip() else None
            })
            
            # Configurar cookie
            response.set_cookie(
                'usuario',
                value=data['nome'],
                max_age=7*24*60*60,  # 7 dias em segundos
                httponly=False,  # Permitir acesso via JavaScript
                samesite='Lax'
            )
            
            response.set_cookie(
                'tipo_usuario',
                value=data['tipo'],
                max_age=7*24*60*60,
                httponly=False,
                samesite='Lax'
            )
            
            return response
        else:
            # Tentar obter detalhes do erro
            error_details = res.text
            try:
                error_json = res.json()
                error_details = str(error_json)
            except:
                pass
            
            return jsonify({
                "status": "erro", 
                "detalhes": f"Erro ao cadastrar no Supabase: {error_details}"
            }), res.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({"status": "erro", "detalhes": "Timeout ao conectar com o Supabase"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"status": "erro", "detalhes": "Erro de conexão com o Supabase"}), 502
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": f"Erro interno: {str(e)}"}), 500

@app.route("/verificar-cookie", methods=["GET"])
def verificar_cookie():
    """Rota para verificar se os cookies estão funcionando"""
    usuario = request.cookies.get('usuario', 'Não encontrado')
    tipo = request.cookies.get('tipo_usuario', 'Não encontrado')
    
    return jsonify({
        "status": "ok",
        "cookies": {
            "usuario": usuario,
            "tipo_usuario": tipo
        },
        "todos_cookies": dict(request.cookies)
    })

@app.route("/limpar-cookie", methods=["POST"])
def limpar_cookie():
    """Rota para limpar cookies"""
    response = jsonify({"status": "ok", "message": "Cookies limpos"})
    response.delete_cookie('usuario')
    response.delete_cookie('tipo_usuario')
    return response

@app.route("/listar-cadastros", methods=["GET"])
def listar_cadastros():
    """Rota para listar todos os cadastros (para teste)"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/cadastro?select=*"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            return jsonify({"status": "ok", "data": res.json()})
        else:
            return jsonify({"status": "erro", "detalhes": res.text}), res.status_code
            
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/chatforum")
def chat_forum():
    return render_template("chatforum.html")

@app.route("/teste", methods=["GET"])
def teste():
    """Rota de teste para verificar se o Flask está funcionando"""
    return jsonify({
        "status": "online",
        "mensagem": "Flask está funcionando",
        "supabase_url_configurada": SUPABASE_URL is not None,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/teste-supabase", methods=["GET"])
def teste_supabase():
    """Rota para testar conexão com o Supabase"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        res = requests.get(url, headers=headers, timeout=5)
        
        return jsonify({
            "status": "ok" if res.status_code == 200 else "erro",
            "status_code": res.status_code,
            "conexao_supabase": "OK" if res.status_code == 200 else "FALHA"
        })
        
    except Exception as e:
        return jsonify({
            "status": "erro",
            "conexao_supabase": "FALHA",
            "detalhes": str(e)
        }), 500

if __name__ == "__main__":
    print("=" * 50)
    print("INICIANDO SERVIDOR FLASK")
    print(f"Supabase URL: {SUPABASE_URL[:30]}...")
    print("Rotas disponíveis:")
    print("  GET  /                    - Página inicial")
    print("  GET  /cadastro            - Formulário de cadastro")
    print("  POST /cadastro            - Enviar cadastro")
    print("  GET  /verificar-cookie    - Verificar cookies")
    print("  GET  /teste               - Teste do servidor")
    print("  GET  /teste-supabase      - Teste do Supabase")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
