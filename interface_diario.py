# interface_diario.py
from datetime import datetime
import sqlite3
import tkinter as tk
import datetime as dt
from db import criar_tabela_diario, adicionar_entrada_diario, obter_entradas_diario, editar_entrada_diario, excluir_entrada_diario

class TelaDiario(tk.Toplevel):
    def __init__(self, master=None, usuario_id=None):
        super().__init__(master)
        self.usuario_id = usuario_id
        self.datetime_label = tk.Label(self, text="")
        self.datetime_label.pack(pady=10)
        criar_tabela_diario()

        # Componentes da interface do diário
        self.title_label = tk.Label(self, text="Título:")
        self.title_entry = tk.Entry(self)

        self.my_title = tk.Label(self, text="My Confidence")
        self.my_title.pack(pady=5)

        self.body_label = tk.Label(self, text="Corpo:")
        self.body_text = tk.Text(self, height=10, width=30)

        # Botões
        self.add_entry_button = tk.Button(self, text="Adicionar Entrada", command=self.adicionar_entrada)
        self.edit_entry_button = tk.Button(self, text="Editar Entrada", command=self.abrir_janela_edicao)
        self.delete_entry_button = tk.Button(self, text="Excluir Entrada", command=self.excluir_entrada)

        # Listbox para exibir as entradas
        self.entries_listbox = tk.Listbox(self, selectmode=tk.SINGLE, width=40)
        self.entries_listbox.bind('<<ListboxSelect>>', self.mostrar_entrada_selecionada)
        self.entries_listbox.bind('<Double-1>', self.mostrar_entrada_detalhes)

        # Janela de edição
        self.janela_edicao = None
        self.title_label_edicao = None
        self.title_entry_edicao = None
        self.body_label_edicao = None
        self.body_text_edicao = None
        self.salvar_button = None
        self.cancelar_button = None

        # Variáveis para armazenar detalhes da entrada selecionada
        self.selected_entry_details = None

        # Posicionamento dos componentes na interface
        self.title_label.pack(pady=10)
        self.title_entry.pack(pady=20)
        self.body_label.pack(pady=10)
        self.body_text.pack(pady=20)
        self.add_entry_button.pack(pady=5)
        self.edit_entry_button.pack(pady=5)
        self.delete_entry_button.pack(pady=5)
        self.entries_listbox.pack(pady=20)

        # Carrega as entradas existentes
        self.carregar_entradas()
        
    def abrir_interface_diario(usuario_id):
        root = TelaDiario(usuario_id=usuario_id)
        root.mainloop()

        

    def adicionar_entrada(self):
        titulo = self.title_entry.get()
        corpo = self.body_text.get("1.0", tk.END)  # Obtém todo o texto do componente Text
        

        # Obtém a data e hora atuais
        data_registro = dt.datetime.today().strftime("%Y-%m-%d")
        hora_registro = dt.datetime.now().strftime("%H:%M:%S")
        usuario_id = "Local user"  # ID usuário logado
        usuario_id = self.usuario_id
    
        adicionar_entrada_diario(titulo, corpo, data_registro, hora_registro, usuario_id)
        self.carregar_entradas()

        # Atualiza o rótulo de data e hora
        self.datetime_label.config(text=f"Data: {data_registro}  Hora: {hora_registro}")

        # Limpa os campos
        self.title_entry.delete(0, tk.END)
        self.body_text.delete("1.0", tk.END)

    def carregar_entradas(self):
        self.entries_listbox.delete(0, tk.END)
        entradas = obter_entradas_diario(self.usuario_id)
        for entrada in entradas:
            titulo = entrada[1]
            data_registro = entrada[3]
            hora_registro = entrada[4]
            self.entries_listbox.insert(tk.END, f"{titulo} - Data: {data_registro} Hora: {hora_registro}")


    def mostrar_entrada_selecionada(self, event):
        selected_index = self.entries_listbox.curselection()
        
        if selected_index:
            self.entry_id = obter_entradas_diario(self.usuario_id)[selected_index[0]][0]
            self.selected_entry_details = obter_detalhes_entrada_diario(self.entry_id)
            # Adicione lógica para exibir os detalhes da entrada, se necessário

    def mostrar_entrada_detalhes(self, event):
        selected_index = self.entries_listbox.curselection()
        if selected_index:
            self.entry_id = obter_entradas_diario(self.usuario_id)[selected_index[0]][0]
            self.selected_entry_details = obter_detalhes_entrada_diario(self.entry_id)

            # Chama a função para abrir a janela de detalhes
            self.abrir_janela_detalhes()

    # ...

    def abrir_janela_detalhes(self):
    # Criação da janela de detalhes
        janela_detalhes = tk.Toplevel(self)
        janela_detalhes.title("Detalhes da Entrada")

         # Componentes da janela de detalhes
        titulo_label = tk.Label(janela_detalhes, text="Título:")
        titulo_label.grid(row=0, column=0, pady=5)

        corpo_label = tk.Label(janela_detalhes, text="Corpo:")
        corpo_label.grid(row=1, column=0, pady=5)

         # Exibe os detalhes da entrada na janela
        titulo_texto = tk.Label(janela_detalhes, text=self.selected_entry_details['titulo'])
        titulo_texto.grid(row=0, column=1, pady=5)

        corpo_texto = tk.Label(janela_detalhes, text=self.selected_entry_details['corpo'], wraplength=400)
        corpo_texto.grid(row=1, column=1, pady=5)

        # Calcula a altura necessária com base no comprimento do texto
        altura_texto = corpo_texto.winfo_reqheight()

        # Ajusta automaticamente a altura da janela com uma margem
        janela_detalhes.geometry(f"400x{altura_texto + 50}")

    def abrir_janela_edicao(self):
        if self.selected_entry_details:
            # Criação da janela de edição
            self.janela_edicao = tk.Toplevel(self)
            self.janela_edicao.title("Editar Entrada")

            # Componentes da janela de edição
            self.title_label_edicao = tk.Label(self.janela_edicao, text="Novo Título:")
            self.title_entry_edicao = tk.Entry(self.janela_edicao, width=30)
            self.title_entry_edicao.insert(tk.END, self.selected_entry_details['titulo'])

            self.body_label_edicao = tk.Label(self.janela_edicao, text="Novo Corpo:")
            self.body_text_edicao = tk.Text(self.janela_edicao, height=10, width=30)
            self.body_text_edicao.insert(tk.END, self.selected_entry_details['corpo'])

            # Botões na janela de edição
            self.salvar_button = tk.Button(self.janela_edicao, text="Salvar", command=self.salvar_edicao)
            self.cancelar_button = tk.Button(self.janela_edicao, text="Cancelar", command=self.destroy_janela_edicao)

            # Posicionamento dos componentes na janela de edição
            self.title_label_edicao.grid(row=0, column=0, pady=5)
            self.title_entry_edicao.grid(row=0, column=1, pady=5)
            self.body_label_edicao.grid(row=1, column=0, pady=5)
            self.body_text_edicao.grid(row=1, column=1, pady=5)
            self.salvar_button.grid(row=2, column=0, pady=5)
            self.cancelar_button.grid(row=2, column=1, pady=5)

    # Função para editar uma entrada no diário
    def editar_entrada_diario(self, entry_id, novo_titulo, novo_corpo, data_registro, hora_registro):
        conexao = sqlite3.connect("diario.db")
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE diario
            SET titulo=?, corpo=?, data_registro=?, hora_registro=?
            WHERE id=?
        """, (novo_titulo, novo_corpo, data_registro, hora_registro, entry_id))

        conexao.commit()
        conexao.close()

    def salvar_edicao(self):
        novo_titulo = self.title_entry_edicao.get()
        novo_corpo = self.body_text_edicao.get("1.0", tk.END)

        # Obtém a data e hora atuais
        data_registro = dt.datetime.today().strftime("%Y-%m-%d")
        hora_registro = dt.datetime.now().strftime("%H:%M:%S")

        self.editar_entrada_diario(self.entry_id, novo_titulo, novo_corpo, data_registro, hora_registro)
        self.carregar_entradas()
        self.destroy_janela_edicao()

    def destroy_janela_edicao(self):
        # Destroi a janela de edição
        if self.janela_edicao:
            self.janela_edicao.destroy()
            self.janela_edicao = None
            self.title_label_edicao = None
            self.title_entry_edicao = None
            self.body_label_edicao = None
            self.body_text_edicao = None
            self.salvar_button = None
            self.cancelar_button = None

    def excluir_entrada(self):
        if hasattr(self, 'entry_id'):
            excluir_entrada_diario(self.entry_id)
            self.carregar_entradas()

# Função para obter detalhes da entrada pelo ID
def obter_detalhes_entrada_diario(entry_id):
    conexao = sqlite3.connect("diario.db")
    cursor = conexao.cursor()


    cursor.execute("SELECT * FROM diario WHERE id=?", (entry_id,))
    entrada = cursor.fetchone()

    conexao.close()

    # Retorna um dicionário com os detalhes da entrada
    if entrada:
        return {
            'titulo': entrada[1],
            'corpo': entrada[2],
            'data_registro': entrada[3],
            'hora_registro': entrada[4],
            'usuario_id': entrada[5]
        }
    else:

        return None
