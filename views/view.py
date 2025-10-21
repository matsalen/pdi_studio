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

        # Prioriza empacotar o painel de controle primeiro para reservar espaço do log
        self.control_panel.frame.pack(side="right", fill="y")
        self.image_panel.frame.pack(side="left", fill="both", expand=True)

    '''def display_image(self, image):
        self.image_panel.show_image(image)'''

    # Exibe a imagem original
    def display_original(self, image):
        self.image_panel.show_original(image)

    # Exibe a imagem processada
    def display_processada(self, image):
        self.image_panel.show_processada(image)

    def log_action(self, text):
        self.control_panel.add_log(text)
