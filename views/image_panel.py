import customtkinter as ctk
# A gente usa o 'Label' do 'tk' normal (o antigo)
# pq o 'CTkLabel' (o novo) é meio chato/bugado
# pra ficar trocando de imagem toda hora.
# Assim, a gente tem a moldura bonita (CTk) e
# a tela funcional (tk).
from tkinter import Label

class ImagePanel:
    # Esse é o 'cinema' do app. O painelzão da esquerda
    # que segura as duas 'telas' (original e processada).
    def __init__(self, root):
        
        # O 'main_frame' é a moldura de fora.
        # É o que a View 'gruda' na esquerda da janela.
        self.main_frame = ctk.CTkFrame(root)

        # --- A tela da ESQUERDA (Original) ---
        # 1. A moldurinha interna da original
        self.frame_original = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        # 2. A 'tela' de verdade (o 'canvas').
        #    É um 'tk.Label' normal, mas disfarçado com o fundo escuro.
        self.label_original = Label(self.frame_original, bg="#242424", text="")
        self.label_original.pack(fill="both", expand=True) # Preenche o frame

        # --- A tela da DIREITA (Processada) ---
        # 1. A moldurinha interna da processada
        self.frame_processada = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        # 2. A 'tela' de verdade (o 'canvas') da processada
        self.label_processada = Label(self.frame_processada, bg="#242424", text="")
        self.label_processada.pack(fill="both", expand=True) # Preenche o frame

        # --- O "Tetris" (O Layout 50/50) ---
        # Aqui é o 'pulo do gato'. A gente usa .grid()
        # DENTRO do 'main_frame' pra forçar a divisão.
        
        # Original: (linha 0, coluna 0)
        self.frame_original.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Processada: (linha 0, coluna 1)
        self.frame_processada.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # O 'segredo' pro 50/50:
        # A gente fala pro 'main_frame':
        # "Dê peso 1 pra coluna 0..."
        self.main_frame.grid_columnconfigure(0, weight=1)
        # "...e dê peso 1 pra coluna 1."
        self.main_frame.grid_columnconfigure(1, weight=1)
        # Resultado: Elas brigam por espaço e empatam, dividindo no meio.
        
        # Manda a linha 0 (a única que tem) crescer pra preencher a altura.
        self.main_frame.grid_rowconfigure(0, weight=1)


    # show_image: O "delivery" da foto original.
    # O Controller chama isso pra botar a foto na tela da esquerda.
    def show_image(self, image):
        self.label_original.config(image=image)
        # LINHA VITAL: Isso impede o 'lixeiro' (Garbage Collector)
        # do Python de apagar a imagem da memória. Sem isso, a imagem some.
        self.label_original.image = image  

    # show_processada: O "delivery" da foto zoada.
    # O Controller chama isso pra botar a foto na tela da direita.
    def show_processada(self, image):
        self.label_processada.config(image=image)
        # Mesma mágica do lixeiro aqui.
        self.label_processada.image = image