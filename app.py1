from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
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

if __name__ == "__main__":
    app.run(debug=True)
