# db.py
import sqlite3

def criar_tabela_usuarios():
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            senha TEXT
        )
    ''')

    conexao.commit()
    conexao.close()

def criar_tabela_diario():
    conexao = sqlite3.connect("diario.db")
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            corpo TEXT,
            data_registro TEXT,
            hora_registro TEXT,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')

    conexao.commit()
    conexao.close()

def adicionar_entrada_diario(titulo, corpo, data_registro, hora_registro, usuario_id):
    conexao = sqlite3.connect("diario.db")
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO diario (titulo, corpo, data_registro, hora_registro, usuario_id) VALUES (?, ?, ?, ?, ?)",
                   (titulo, corpo, data_registro, hora_registro, usuario_id))

    conexao.commit()
    conexao.close()
    
def obter_entradas_diario(usuario_id):
    conexao = sqlite3.connect("diario.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM diario WHERE usuario_id=?", (usuario_id,))
    entradas = cursor.fetchall()

    conexao.close()
    return entradas

def editar_entrada_diario(entry_id, novo_titulo, novo_corpo):
    conexao = sqlite3.connect("diario.db")
    cursor = conexao.cursor()

    cursor.execute("UPDATE diario SET titulo=?, corpo=? WHERE id=?", (novo_titulo, novo_corpo, entry_id))

    conexao.commit()
    conexao.close()

def excluir_entrada_diario(entry_id):
    conexao = sqlite3.connect("diario.db")
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM diario WHERE id=?", (entry_id,))

    conexao.commit()
    conexao.close()

def realizar_login(username, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE username=? AND senha=?", (username, senha))
    usuario_id = cursor.fetchone()

    conexao.close()
    return usuario_id

def adicionar_usuario(username, senha):
    try:
        conexao = sqlite3.connect("usuarios.db")
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, senha))

        conexao.commit()
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")
    finally:
        conexao.close()
        
        