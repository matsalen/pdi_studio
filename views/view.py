import tkinter as tk
from views.menu_bar import MenuBar
from views.image_panel import ImagePanel
from views.control_panel import ControlPanel

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Menu superior
        self.menu = MenuBar(self.root, controller)
        self.root.config(menu=self.menu.menubar)

        # Painéis
        self.image_panel = ImagePanel(self.root)
        self.control_panel = ControlPanel(self.root)

        # Painel histograma
        self.right_sidebar_frame = tk.Frame(self.root, bg="#333") 
        self.tools_panel = tk.Frame(self.right_sidebar_frame, bg="#444", height=200)

        # 1. Crie os contêineres
        self.right_sidebar_frame = tk.Frame(self.root, width=300) 
        self.control_panel = ControlPanel(self.right_sidebar_frame) 
        self.tools_panel = tk.Frame(self.right_sidebar_frame, height=250) 

        # 2. Crie o display do histograma DENTRO do tools_panel
        self.histogram_label = tk.Label(self.tools_panel, bg="#222")
        self.histogram_label.pack(fill="both", expand=True, padx=5, pady=5)

        # --- ORDEM DE EMPACOTAMENTO CORRETA ---

        # 3. EMPACOTE A BARRA LATERAL PRIMEIRO (na direita)
        self.right_sidebar_frame.pack(side="right", fill="y")
        self.right_sidebar_frame.pack_propagate(False) 

        # 4. EMPACOTE O PAINEL DE IMAGEM DEPOIS (na esquerda)
        self.image_panel.main_frame.pack(side="left", fill="both", expand=True)

        # --- EMPACOTAMENTO DENTRO DA BARRA LATERAL ---

        # 5. Coloque o painel de ferramentas EMBAIXO, com altura fixa
        self.tools_panel.pack(side="bottom", fill="x")
        self.tools_panel.pack_propagate(False) 

        # 6. Coloque os logs EM CIMA, preenchendo o resto
        self.control_panel.frame.pack(side="top", fill="both", expand=True)        

    def display_image(self, image):
        self.image_panel.show_image(image)

    def display_image_proc(self, image):
        self.image_panel.show_processada(image)

    def display_histogram(self, histogram_image):
        """ Coloca a imagem do gráfico no painel de ferramentas. """
        self.histogram_label.config(image=histogram_image)
        self.histogram_label.image = histogram_image # Mantém a referência

    def log_action(self, text):
        self.control_panel.add_log(text)