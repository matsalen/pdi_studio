import tkinter as tk
from tkinter import scrolledtext

class ControlPanel:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="#333", width=250)
        self.frame.pack_propagate(False)

        tk.Label(self.frame, text="Histórico de Ações", fg="white", bg="#333").pack(pady=5)
        self.log_area = scrolledtext.ScrolledText(self.frame, width=35, height=30, bg="#111", fg="white")
        self.log_area.pack(padx=5, pady=5)

    def add_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)
