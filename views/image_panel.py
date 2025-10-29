import tkinter as tk
from tkinter import Label

class ImagePanel:
    def __init__(self, root):
        # 1. O contêiner principal. Isso não muda.
        # (Voltando a cor para #222 para combinar)
        self.main_frame = tk.Frame(root, bg="#222")

        # 2. Os frames filhos. Isso não muda.
        self.frame_original = tk.Frame(self.main_frame, bg="#222")
        self.label_original = Label(self.frame_original, bg="#222")
        # O label dentro do frame_original pode continuar com .pack()
        self.label_original.pack(fill="both", expand=True) 

        self.frame_processada = tk.Frame(self.main_frame, bg="#222")
        self.label_processada = Label(self.frame_processada, bg="#222")
        # O label dentro do frame_processada também
        self.label_processada.pack(fill="both", expand=True)

        # 3. A MUDANÇA: Use .grid() para organizar os frames DENTRO do main_frame
        
        # self.frame_original.pack(side="left", fill="both", expand=True)   <-- REMOVA
        # self.frame_processada.pack(side="left", fill="both", expand=True)  <-- REMOVA

        # Coloque o frame original na linha 0, coluna 0
        self.frame_original.grid(row=0, column=0, sticky="nsew")
        # Coloque o frame processado na linha 0, coluna 1
        self.frame_processada.grid(row=0, column=1, sticky="nsew")

        # 4. CONFIGURE AS COLUNAS: Diga ao main_frame para dar peso igual (1)
        #    a ambas as colunas, forçando-as a dividir o espaço
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Diga também para a linha 0 expandir verticalmente
        self.main_frame.grid_rowconfigure(0, weight=1)


    def show_image(self, image):
        self.label_original.config(image=image)
        self.label_original.image = image  # mantém referência

    def show_processada(self, image):
        self.label_processada.config(image=image)
        self.label_processada.image = image