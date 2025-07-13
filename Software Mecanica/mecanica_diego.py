import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

class MecanicaDiego:
    def __init__(self, master):
        self.master = master
        self.master.title("Mecânica Diego - Cadastro de Clientes")
        self.master.geometry("550x400")

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

        self.btn_salvar = tk.Button(self.master, text="Gerar Ordem de Serviço (TXT)", command=self.gerar_os_txt)
        self.btn_salvar.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def gerar_os_txt(self):
        dados = {key: entry.get() for key, entry in self.entries.items()}

        if any(not valor.strip() for valor in dados.values()):
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        # === Número sequencial da OS ===
        num_os = self.get_num_os()

        # === Texto da Ordem de Serviço ===
        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')

        os_texto = (
            f"===== Mecânica Diego =====\n"
            f"Ordem de Serviço Nº {num_os}\n"
            f"Data/Hora: {data_atual}\n"
            f"--------------------------\n"
        )

        for chave, valor in dados.items():
            os_texto += f"{chave} {valor}\n"

        os_texto += "==========================\n"

        nome_arquivo = f"OS_{num_os}_{dados['Placa:']}.txt"

        with open(nome_arquivo, "w") as f:
            f.write(os_texto)

        messagebox.showinfo("Sucesso", f"Ordem de Serviço gerada!\nArquivo: {nome_arquivo}")

        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def get_num_os(self):
        arquivo = "numero_os.txt"

        if not os.path.exists(arquivo):
            with open(arquivo, "w") as f:
                f.write("1")
            return 1
        else:
            with open(arquivo, "r") as f:
                num = int(f.read().strip())

            num += 1

            with open(arquivo, "w") as f:
                f.write(str(num))

            return num

def main():
    root = tk.Tk()
    app = MecanicaDiego(root)
    root.mainloop()

if __name__ == "__main__":
    main()
