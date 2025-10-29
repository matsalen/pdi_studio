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

        # Prioriza empacotar o painel de controle primeiro
        self.control_panel.frame.pack(side="right", fill="y")
        
        # AGORA, empacote apenas o main_frame do image_panel
        # Ele vai pegar todo o espaço restante e preenchê-lo
        self.image_panel.main_frame.pack(side="left", fill="both", expand=True)
        
        # Essas linhas abaixo não são mais necessárias aqui, 
        # pois já foram feitas dentro do __init__ de ImagePanel
        # self.image_panel.frame_original.pack(side="left", fill="both", expand=True)
        # self.image_panel.frame_processada.pack(side="left", fill="both", expand=True)

    def display_image(self, image):
        self.image_panel.show_image(image)

    def display_image_proc(self, image):
        self.image_panel.show_processada(image)

    def log_action(self, text):
        self.control_panel.add_log(text)