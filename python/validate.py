from flask import Flask, request, render_template_string
import sqlite3
import re

app = Flask(__name__)

def validar_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

def validar_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def validar_telefone(telefone):
    return len(telefone) == 11 and telefone.isdigit()

def conectar_banco():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

def inserir_usuario(conn, cursor, nome, cpf, email, telefone, endereco):
    try:
        cursor.execute('''
            INSERT INTO usuarios (nome, cpf, email, telefone, endereco)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, cpf, email, telefone, endereco))
        conn.commit()
        return "Usuário cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return "Erro: CPF ou e-mail já cadastrado."

# Rota principal para exibir o formulário
@app.route('/')
def form():
    return render_template_string(open('pages/login.html').read())

@app.route('/processar_login', methods=['POST'])
def processar_login():
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']

    if not validar_cpf(cpf):
        return "Erro: CPF inválido. O CPF deve ter 11 dígitos numéricos."
    if not validar_email(email):
        return "Erro: E-mail inválido. Por favor, forneça um e-mail válido."
    if not validar_telefone(telefone):
        return "Erro: Telefone inválido. O telefone deve ter 11 dígitos numéricos."

    conn, cursor = conectar_banco()
    mensagem = inserir_usuario(conn, cursor, nome, cpf, email, telefone, endereco)

    conn.close()
    return mensagem

if __name__ == "__main__":
    app.run(debug=True)
