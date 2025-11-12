import customtkinter as ctk  
import tkinter as tk         # Precisamos dos dois, o 'ctk' pra beleza, o 'tk' pro que funciona (menu e label de img)
from views.menu_bar import MenuBar
from views.image_panel import ImagePanel
from views.control_panel import ControlPanel

class View:
    # __init__: Onde a gente "desenha" a tela toda.
    def __init__(self, root, controller):
        self.root = root # 'root' é a janela principal que o Controller criou
        self.controller = controller # A gente guarda o 'controller' pra saber quem chamar

        # O menu lá de cima (Arquivo, Filtros, etc.)
        # É o único treco 'tk' feioso que sobrou, mas funciona.
        self.menu = MenuBar(self.root, controller)
        self.root.config(menu=self.menu.menubar)

        # O painelzão da esquerda, que segura as duas imagens
        self.image_panel = ImagePanel(self.root) 

        # --- A Barra da Direita ---
        # A gente cria um "super-frame" pra segurar tudo que vai na direita.
        self.right_sidebar_frame = ctk.CTkFrame(self.root, width=300)
        
        # O painel de logs (o fofoqueiro) vai DENTRO da sidebar
        self.control_panel = ControlPanel(self.right_sidebar_frame) 
        
        # O painel de "ferramentas" (sliders/hist) também vai DENTRO da sidebar
        self.tools_panel = ctk.CTkFrame(self.right_sidebar_frame, height=350) 

        # --- Recheio do Painel de Ferramentas ---
        
        ctk.CTkLabel(self.tools_panel, text="Ajustes Manuais", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)

        # Slider de Contraste
        ctk.CTkLabel(self.tools_panel, text="Contraste (α)").pack(fill='x', padx=15, pady=(5,0))
        self.contrast_slider = ctk.CTkSlider(self.tools_panel,
                                             from_=0.1, to=3.0,
                                             number_of_steps=29) # 29 passinhos
        self.contrast_slider.set(1.0) # Começa no '1.0' (normal)
        self.contrast_slider.pack(fill='x', padx=15, pady=(0, 10))

        # Slider de Brilho
        ctk.CTkLabel(self.tools_panel, text="Brilho (β)").pack(fill='x', padx=15, pady=(5,0))
        self.brightness_slider = ctk.CTkSlider(self.tools_panel,
                                               from_=-100, to=100,
                                               number_of_steps=200) # 200 passinhos
        self.brightness_slider.set(0) # Começa no '0' (normal)
        self.brightness_slider.pack(fill='x', padx=15, pady=(0, 10))
        
        # Onde o gráfico do histograma vai aparecer.
        # É um Label 'tk' normal, mas disfarçado de 'ctk' (com a cor do fundo).
        # (O Label do 'ctk' é meio chato pra atualizar imagem rápido)
        self.histogram_label = tk.Label(self.tools_panel, bg="#2B2B2B") 
        self.histogram_label.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Empacotamento Final (O "Tetris") ---
        # Aqui a gente diz quem fica onde. A ordem importa!
        
        # 1. Barra da direita: gruda na DIREITA, preenche o Y
        self.right_sidebar_frame.pack(side="right", fill="y")
        self.right_sidebar_frame.pack_propagate(False) # "Não encolha, mantenha seus 300px!"
        
        # 2. Painel de imagem: gruda na ESQUERDA, e pega TODO o resto do espaço
        self.image_panel.main_frame.pack(side="left", fill="both", expand=True)
        
        # 3. DENTRO da barra da direita:
        #    Painel de ferramentas: gruda EMBAIXO
        self.tools_panel.pack(side="bottom", fill="x")
        self.tools_panel.pack_propagate(False) # "Não encolha, mantenha seus 350px!"
        
        #    Painel de logs: gruda EM CIMA e pega o resto do espaço da sidebar
        self.control_panel.frame.pack(side="top", fill="both", expand=True)

    # --- Métodos "Burros" ---
    # São as ordens que o Controller pode gritar pra View.
    # A View só obedece.

    def display_image(self, image):
        # "View, bote esta imagem na esquerda!"
        self.image_panel.show_image(image)

    def display_image_proc(self, image):
        # "View, bote esta imagem na direita!"
        self.image_panel.show_processada(image)

    def display_histogram(self, histogram_image):
        # "View, bote este gráfico no painel!"
        self.histogram_label.config(image=histogram_image)
        self.histogram_label.image = histogram_image # "Não apague a imagem, lixeiro!" (evita o garbage collector)

    def reset_sliders(self):
        # "View, volte os sliders pro padrão!"
        self.contrast_slider.set(1.0)
        self.brightness_slider.set(0)

    def log_action(self, text):
        # "View, anote esta fofoca no log!"
        self.control_panel.add_log(text)