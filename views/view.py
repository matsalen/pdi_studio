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
        self.tools_panel = tk.Frame(self.right_sidebar_frame, height=350) 

        # --- NOVOS WIDGETS DE SLIDER ---
        # (Coloque-os DENTRO do self.tools_panel)
        
        # Label do Frame
        tk.Label(self.tools_panel, text="Ajustes", font=("Arial", 10, "bold")).pack(pady=5)

        # Contraste (Alpha)
        # Range de 0.1 (sem contraste) a 3.0 (alto contraste)
        self.contrast_slider = tk.Scale(self.tools_panel,
                                        from_=0.1, to=3.0, resolution=0.1,
                                        orient="horizontal", label="Contraste (α)",
                                        length=280)
        self.contrast_slider.set(1.0) # Valor padrão
        self.contrast_slider.pack(fill='x', padx=5)

        # Brilho (Beta)
        # Range de -100 (escuro) a 100 (claro)
        self.brightness_slider = tk.Scale(self.tools_panel,
                                          from_=-100, to=100,
                                          orient="horizontal", label="Brilho (β)",
                                          length=280)
        self.brightness_slider.set(0) # Valor padrão
        self.brightness_slider.pack(fill='x', padx=5)
        
        # O Label do Histograma (agora vai embaixo dos sliders)
        self.histogram_label = tk.Label(self.tools_panel, bg="#222")
        self.histogram_label.pack(fill="both", expand=True, padx=5, pady=5)

        # --- (Resto do seu código de empacotamento) ---
        self.right_sidebar_frame.pack(side="right", fill="y")
        self.right_sidebar_frame.pack_propagate(False)
        self.image_panel.main_frame.pack(side="left", fill="both", expand=True)
        self.tools_panel.pack(side="bottom", fill="x")
        self.tools_panel.pack_propagate(False)
        self.control_panel.frame.pack(side="top", fill="both", expand=True)       

    def display_image(self, image):
        self.image_panel.show_image(image)

    def display_image_proc(self, image):
        self.image_panel.show_processada(image)

    def display_histogram(self, histogram_image):
        """ Coloca a imagem do gráfico no painel de ferramentas. """
        self.histogram_label.config(image=histogram_image)
        self.histogram_label.image = histogram_image # Mantém a referência

    # --- NOVO MÉTODO ---
    def reset_sliders(self):
        """ Reseta os sliders para os valores padrão. """
        self.contrast_slider.set(1.0)
        self.brightness_slider.set(0)

    def log_action(self, text):
        self.control_panel.add_log(text)