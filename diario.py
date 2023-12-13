# diario.py
import sqlite3

def adicionar_entrada_diario(titulo, corpo, data_registro, hora_registro, usuario_id):
    conexao = sqlite3.connect("diario.db")
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO diario (titulo, corpo, data_registro, hora_registro, usuario_id) VALUES (?, ?, ?, ?, ?)",
                   (titulo, corpo, data_registro, hora_registro, usuario_id))

    conexao.commit()
    conexao.close()
