import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class MecanicaDiego:
    def __init__(self, master):
        self.master = master
        self.master.title("Mecânica Diego - Cadastro de Clientes")
        self.master.geometry("550x400")

        # Inicializa o banco de dados
        self.init_db()

        self.create_widgets()

    def create_widgets(self):
        labels = ["Nome:", "Telefone:", "Placa:", "Modelo:", "Ano:", "Cor:", "Tipo de Serviço:"]
        self.entries = {}

        for idx, text in enumerate(labels):
            label = tk.Label(self.master, text=text)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

            entry = tk.Entry(self.master, width=45)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

            self.entries[text] = entry

        self.btn_salvar = tk.Button(self.master, text="Salvar no Banco", command=self.salvar_banco)
        self.btn_salvar.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def init_db(self):
        self.conn = sqlite3.connect("mecanica_diego.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ordens_servico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT,
                nome TEXT,
                telefone TEXT,
                placa TEXT,
                modelo TEXT,
                ano TEXT,
                cor TEXT,
                tipo_servico TEXT
            )
        """)
        self.conn.commit()

    def salvar_banco(self):
        dados = {key: entry.get() for key, entry in self.entries.items()}

        if any(not valor.strip() for valor in dados.values()):
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.cursor.execute("""
            INSERT INTO ordens_servico (data_hora, nome, telefone, placa, modelo, ano, cor, tipo_servico)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data_hora,
            dados['Nome:'],
            dados['Telefone:'],
            dados['Placa:'],
            dados['Modelo:'],
            dados['Ano:'],
            dados['Cor:'],
            dados['Tipo de Serviço:']
        ))

        self.conn.commit()

        # Recupera o ID da OS recém inserida
        num_os = self.cursor.lastrowid

        # Opcional: salvar um arquivo .txt também
        nome_arquivo = f"OS_{num_os}_{dados['Placa:']}.txt"
        os_texto = (
            f"===== Mecânica Diego =====\n"
            f"Ordem de Serviço Nº {num_os}\n"
            f"Data/Hora: {data_hora}\n"
            f"--------------------------\n"
        )
        for chave, valor in dados.items():
            os_texto += f"{chave} {valor}\n"
        os_texto += "==========================\n"

        with open(nome_arquivo, "w") as f:
            f.write(os_texto)

        messagebox.showinfo("Sucesso", f"Ordem de Serviço salva no banco!\nArquivo gerado: {nome_arquivo}")

        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def __del__(self):
        self.conn.close()

def main():
    root = tk.Tk()
    app = MecanicaDiego(root)
    root.mainloop()

if __name__ == "__main__":
    main()
