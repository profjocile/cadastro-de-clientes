import sqlite3

from bottle import get, post, redirect, request, route, run, template

DB_NAME = 'meu_banco_de_dados2.db'
 
def inicializar_banco():
    """Garante a existência da tabela 'clientes' no banco SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()
 
# 1. ROTA PRINCIPAL: Listagem de Clientes e Formulário de Cadastro

@route('/', method=['GET','POST'])
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email FROM clientes;")
    clientes = cursor.fetchall()
    conn.close()
 
    return template('form_clientes_v3', lista_clientes=clientes)
 
# 2. ROTA DE CADASTRO (Novo Cliente)
@route('/cadastrar', method=['GET','POST'])
def cadastrar():
    nome = request.forms.get('nome')
    email = request.forms.get('email')
 
    if nome and email:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?);", (nome, email))
        conn.commit()
        conn.close()
 
    redirect('/')
 
# 3. ROTA DE EDIÇÃO - EXIBIR FORMULÁRIO (GET)
@get('/editar/<id:int>')
def exibir_formulario_edicao(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email FROM clientes WHERE id = ?;", (id,))
    cliente = cursor.fetchone()
    conn.close()
 
    if not cliente:
        print(f'O id informado não existe: {id}')
        redirect('/')
 
    html_editar = '''
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Editar Cliente</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 30px; }
                h1 { color: #333; }
                form { background: #f4f4f4; padding: 15px; border-radius: 5px; width: 300px; }
                input { margin-bottom: 10px; padding: 8px; width: 90%; display: block; }
                input[type="submit"] { background: #007bff; color: white; border: none; cursor: pointer; width: 100px; }
                a { color: #6c757d; text-decoration: none; display: inline-block; margin-top: 10px; }
            </style>
        </head>
        <body>
            <h1>Editar Cliente #{{cliente[1]}}</h1>
            
            <form action="/editar/{{cliente[0]}}" method="post">
                <label>Nome:</label>
                <input type="text" name="nome" value="{{cliente[1]}}" required>
                
                <label>E-mail:</label>
                <input type="email" name="email" value="{{cliente[2]}}" required>
                
                <input type="submit" value="Salvar">
            </form>
 
            <a href="/">← Cancelar e Voltar</a>
        </body>
        </html>
    '''
    return template(html_editar, cliente=cliente)
 
# 4. ROTA DE EDIÇÃO - SALVAR ALTERAÇÕES (POST)
@post('/editar/<id:int>')
def salvar_edicao(id):
    nome = request.forms.get('nome')
    email = request.forms.get('email')
 
    if nome and email:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Atualiza os dados com a instrução SQL UPDATE usando parâmetros seguros
        cursor.execute(
            "UPDATE clientes SET nome = ?, email = ? WHERE id = ?;",
            (nome, email, id)
        )
        conn.commit()
        conn.close()
 
    redirect('/')
 
# 5. ROTA DE EXCLUSÃO
@route('/deletar/<id:int>', method=['GET','POST'])
def deletar(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?;", (id,))
    conn.commit()
    conn.close()
    
    redirect('/')
 
if __name__ == '__main__':
    inicializar_banco()
    print("Servidor rodando em http://localhost:8080 ...")
    run(host='localhost', port=8080, debug=True, reloader=True)