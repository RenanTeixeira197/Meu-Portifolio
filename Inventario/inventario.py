import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


class MeuInventario():
    def __init__(self, master):
        self.master = master
        self.master.title("Meu Inventario - Livros e Mangás")
        self.master.geometry("660x500")

        self.__init__db()

        self.create_widgets()
    
    def create_widgets(self):
        labels = ["Nome: ", "Tipo", "Volumes", "Volumes Adquiridos"]
        self.entries = {}

        for idx, text in enumerate(labels):
            label = tk.Label(self.master, text="text")
            label.grid(row=idx, column=0, padx=0, pady=5, sticky="e")

            entry = tk.Entry(self.master, width=45)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

            self.entries[text] = entry
        
        self.btn_salvar = tk.Button(self.master, text="Incluir no Banco", command=self.salvar_banco)
        self.btn_salvar.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def init_db(self):
        self.conn = sqlite3.connect("meu_inventario.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INTEGER PRIMARY KEY ATUROINCREMENT,
                data_hora TEXT,
                nome TEXT,
                tipo TEXT,
                volumes TEXT,
                volumes_adquiridos TEXT,
            )
        """)
        self.conn.commit()

    