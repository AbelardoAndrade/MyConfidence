import tkinter as tk
from tkinter import messagebox
from interface_diario import TelaDiario  
from PIL import Image, ImageTk
import sqlite3




class TelaLogin(tk.Tk):
    def __init__(self, master=None, on_close=None):
        super().__init__(master)
        criar_tabela_usuarios()
        self.username = tk.StringVar()
        self.senha = tk.StringVar()
        self.on_close = on_close  # Adiciona o callback
        self.button_login = tk.Button()  # Cria o botão de login

    @staticmethod
    def get_button_login():
        return TelaLogin().button_login  # Retorna o botão de login

    def fechar_janela(self):
        if self.on_close:
            self.on_close(self)
        else:
            self.destroy()

# Função para criar a tabela de usuários no banco de dados
def criar_tabela_usuarios():
    try:
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
    except Exception as e:
        print(f"Erro ao criar tabela de usuários: {e}")
    finally:
        conexao.close()

# Função para adicionar um novo usuário ao banco de dados
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

# Função para verificar as credenciais de login
def realizar_login(username, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE username=? AND senha=?", (username, senha))
    usuario = cursor.fetchone()

    conexao.close()
    return usuario

# Função chamada quando o botão de login é clicado
def fazer_login():
    username = entry_username.get()
    senha = entry_senha.get()

    usuario = realizar_login(username, senha)

    if usuario:
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo, {}".format(username))
        abrir_interface_diario()
    else:
        messagebox.showerror("Login falhou", "Credenciais inválidas")

# Função para abrir a interface do diário
def abrir_interface_diario():
    username = entry_username.get()
    senha = entry_senha.get()

    usuario = realizar_login(username, senha)

    if usuario:
        root.destroy()  # Fechar a janela de login
        janela_diario = TelaDiario(usuario_id=usuario[0])  # Passar o ID do usuário como argumento
        janela_diario.mainloop()
    else:
        messagebox.showerror("Login falhou", "Credenciais inválidas")


# Função chamada quando o botão de registro é clicado
def criar_novo_usuario():
    username = entry_username.get()
    senha = entry_senha.get()

    adicionar_usuario(username, senha)
    messagebox.showinfo("Usuário criado", "Novo usuário {} criado com sucesso!".format(username))

# Criar a tabela de usuários ao iniciar o programa
criar_tabela_usuarios()

# Criar a interface gráfica
root = tk.Tk()
root.title("My Confidence")  # Adicione o título desejado

# Carregar a imagem original
tk.Label(root, text="").pack()
#original_image = Image.open("maple.png")

# Redimensionar a imagem para um novo tamanho (ajuste as dimensões conforme necessário)
#new_size = (100, 100)  # Substitua com o tamanho desejado
#resized_image = original_image.resize(new_size, Image.ANTIALIAS)

# Converter a imagem redimensionada para o formato Tkinter
#tk_image = ImageTk.PhotoImage(resized_image)

# Componente para exibir a imagem
#image_label = tk.Label(root, image=tk_image)
#image_label.pack()

# Espaço entre a imagem e os outros componentes
tk.Label(root, text="").pack()


# Definir cores
root.configure(bg="#CAF0F8")  # Cor de fundo da janela
root.option_add('*TButton*highlightBackground', '#ADE8F4')  # Cor de destaque do botão
root.option_add('*TButton*highlightColor', '#0077B6')  # Cor de destaque do botão

# Componentes da interface
label_username = tk.Label(root, text="Usuário:")
entry_username = tk.Entry(root)

label_senha = tk.Label(root, text="Senha:")
entry_senha = tk.Entry(root, show="*")  # Para esconder a senha

# Botões
button_login = tk.Button(root, text="Login", command=fazer_login)
button_registrar = tk.Button(root, text="Registrar Novo Usuário", command=criar_novo_usuario)

# Posicionamento dos componentes na interface
label_username.pack(pady=10)
entry_username.pack(pady=10)
label_senha.pack(pady=10)
entry_senha.pack(pady=10)
button_login.pack(pady=10)
button_registrar.pack(pady=10)

# Centralizar a janela na tela
largura = 600
altura = 460
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
x = (largura_tela - largura) // 2
y = (altura_tela - altura) // 2
root.geometry(f'{largura}x{altura}+{x}+{y}')

# Executar a interface gráfica
root.mainloop()
