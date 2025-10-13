import tkinter as tk

class MenuBar:
    def __init__(self, root, controller):
        self.controller = controller
        self.menubar = tk.Menu(root)

        # Menu Arquivo
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Abrir", command=controller.open_image)
        file_menu.add_command(label="Salvar como...", command=controller.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=root.quit)
        self.menubar.add_cascade(label="Arquivo", menu=file_menu)

        # Menu Filtros
        filter_menu = tk.Menu(self.menubar, tearoff=0)
        filter_menu.add_command(label="Converter para tons de cinza", command=controller.apply_gray)
        filter_menu.add_command(label="Equalizar histograma", command=controller.apply_equalization)
        self.menubar.add_cascade(label="Filtros", menu=filter_menu)
