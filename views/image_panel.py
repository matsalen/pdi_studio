import tkinter as tk
from tkinter import Label

class ImagePanel:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="#222")
        self.label = Label(self.frame, bg="#222")
        # Preenche o espaço disponível do painel, sem alterar o tamanho do painel de controle
        self.label.pack(fill="both", expand=True)

    def show_image(self, image):
        self.label.config(image=image)
        self.label.image = image  # mantém referência
