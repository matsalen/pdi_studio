import tkinter as tk
from tkinter import Label

class ImagePanel:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="#222")
        '''self.label = Label(self.frame, bg="#222")
        # Preenche o espaço disponível do painel, sem alterar o tamanho do painel de controle
        self.label.pack(fill="both", expand=True)

    def show_image(self, image):
        self.label.config(image=image)
        self.label.image = image  # mantém referência'''

        # Label da imagem original
        self.label_original = Label(
            self.frame,
            bg="#222",
            fg="white",
            text="Imagem Original",
            width=80,   # largura em caracteres
            height=25,  # altura em linhas
            relief="groove"
        )
        self.label_original.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Label da imagem processada
        self.label_processada = Label(
            self.frame,
            bg="#222",
            fg="white",
            text="Imagem Processada",
            width=80,
            height=25,
            relief="groove"
        )
        self.label_processada.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    def show_original(self, image):
        self.label_original.config(image=image, text="")
        self.label_original.image = image

    def show_processada(self, image):
        self.label_processada.config(image=image, text="")
        self.label_processada.image = image
