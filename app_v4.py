"""App versão 4 prevenindo erros de acesso ao Banco de Dados"""
import sqlite3

DB_NAME = 'meu_banco_de_dados.db'

def cadastrar_cliente_seguro(nome, email):
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        criar_tabela(cursor)

        # Executa o comando de inserção
        cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?);", (nome, email))
        
        # Se nenhuma exceção ocorreu, confirma as alterações no banco
        conn.commit()
        print("Cliente cadastrado com sucesso!")
        
    except sqlite3.IntegrityError as e:
        # Reverte as alterações pendentes da transação
        if conn:
            conn.rollback()
        print(f"Erro de integridade (ex: e-mail duplicado): {e}")
        
    except sqlite3.Error as e:
        # Reverte qualquer outra falha no banco de dados
        if conn:
            conn.rollback()
        print(f"Erro operacional no banco de dados: {e}")

        
    finally:
        # Garante a liberação dos recursos e o fechamento da conexão
        if conn:
            conn.close()
            print("Conexão fechada com segurança.")

def criar_tabela(cursor):
    # Cria a tabela caso não exista
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
            );
                ''')

def mostrar():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM clientes;")
        clientes = cursor.fetchall()
        conn.close()
    
        return clientes
    except sqlite3.Error as e:
        # Reverte qualquer outra falha no banco de dados
        if conn:
            conn.rollback()
        print(f"Erro operacional no banco de dados: {e}")
        return ''

def menu():
    while True:
        print("Cadastro de clientes")
        cliente = input('Entre com o nome do cliente: ')
        email = input('Entre com o email do cliente:')
        cadastrar_cliente_seguro(cliente, email)

        continuar = input('Continua? s ou n ')
        if continuar == 'n':
            break

menu()
print(mostrar())