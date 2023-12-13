# main.py

import tkinter as tk
from realizar_login import TelaLogin
from interface_diario import TelaDiario

def abrir_interface_diario(usuario_id):
    root = TelaDiario(usuario_id)
    root.mainloop()

def main():
    # Obtenha o botão de login e o botão de registro
    button_login = TelaLogin.get_button_login()
    button_registrar = TelaLogin.get_button_registrar()

    # Substitua a chamada para abrir a interface do diário
    root = tk.Tk()
    entry_username = tk.Entry()
    button_login.config(command=lambda: abrir_interface_diario(entry_username.get()))
    button_registrar.config(command=lambda: abrir_interface_diario(TelaLogin.username.get()))

    # Execute a interface gráfica de login
    #tela_login = TelaLogin()
    #tela_login.mainloop()

if __name__ == "__main__":
    main()
