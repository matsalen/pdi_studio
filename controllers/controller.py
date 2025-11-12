from tkinter import filedialog, messagebox, simpledialog
import customtkinter as ctk
from models.model import Model
from views.view import View

class Controller:
    # __init__: Onde a mágica começa.
    # É o "construtor" do app. Ele monta a janela principal (root),
    # contrata o Model (o cérebro) e a View (a cara do app).
    def __init__(self):
        self.root = ctk.CTk()
        ctk.set_appearance_mode("dark") # Tema escuro, óbvio.
        ctk.set_default_color_theme("blue")
        self.root.title("PDI Studio - Sistema Interativo de Processamento de Imagens")
        self.root.geometry("1600x900")

        # Contrata o cérebro
        self.model = Model()
        # Contrata a cara (e passa 'self' pra ela saber com quem falar)
        self.view = View(self.root, controller=self)

        # Aqui é a "cola": a gente liga os sliders da View
        # para que ELES chamem a NOSSA função (on_slider_move)
        # toda vez que o usuário mexer neles.
        self.view.contrast_slider.configure(command=self.on_slider_move)
        self.view.brightness_slider.configure(command=self.on_slider_move)

    # run: É o "play" do app.
    # Sem ele, a janela aparece e fecha num piscar de olhos.
    def run(self):
        self.root.mainloop()

    # open_image: Pede pro usuário escolher uma foto.
    def open_image(self):
        path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if path: # (Se o usuário não clicou em "Cancelar")
            # 1. Manda o Model carregar a imagem (ele guarda a original)
            image = self.model.load_image(path)
            # 2. Manda a View exibir a imagem na ESQUERDA
            self.view.display_image(image)
            # 3. Reseta os sliders pra não ficar com lixo da foto anterior
            self.view.reset_sliders() 
            # 4. Truque pra popular o painel da DIREITA:
            #    Aplica um filtro qualquer e depois reseta.
            #    Isso "suja" o painel e depois "limpa",
            #    garantindo que o histograma e a imagem processada
            #    apareçam de primeira.
            self.apply_gray()
            self.reset_image()
            self.view.log_action(f"Imagem carregada: {path}")

    # save_image: Salva o *resultado* (a imagem processada).
    # Pede um nome de arquivo e manda o Model salvar.
    def save_image(self):
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        if path:
            self.model.save_image(path)
            self.view.log_action(f"Imagem salva em: {path}")

    # on_slider_move: A função que faz a mágica dos sliders.
    # É chamada MILHÕES de vezes, toda vez que o mouse arrasta.
    def on_slider_move(self, value):
        
        if self.model.image is None:
            return

        try:
            # 1. Pega os valores ATUAIS dos dois sliders (da View)
            alpha = self.view.contrast_slider.get() # Contraste
            beta = self.view.brightness_slider.get()  # Brilho
            
            # 2. Manda pro Model. O Model *não salva* isso,
            #    ele só aplica na "base" e devolve o resultado.
            tk_main, tk_hist = self.model.adjust_brightness_contrast(alpha, beta)
            
            # 3. Manda pra View (imagem + histograma) em tempo real
            if tk_main:
                self.view.display_image_proc(tk_main)
                self.view.display_histogram(tk_hist)
                
        except Exception as e:
            # A gente ignora erros aqui (pass)
            # pra não travar o app se o usuário
            # mexer o slider mais rápido que o processamento.
            pass
    
    
    # -----------------------------------------------------------------
    # PADRÃO "APLICA FILTRO"
    # Todas as funções 'apply_...' abaixo seguem a MESMA receita:
    # 1. Pede ao Model para fazer a matemática (ex: 'convert_to_gray()').
    # 2. O Model (via _update_and_get_views) retorna DUAS imagens:
    #    (imagem_processada_tk, imagem_histograma_tk)
    # 3. O Controller distribui essas imagens para a View.
    # 4. O Controller manda uma fofoca pro log.
    # -----------------------------------------------------------------

    def apply_gray(self):
        # 1. Pede
        tk_main_image, tk_hist_image = self.model.convert_to_gray()
        # 3. Distribui
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)        
        # 4. Fofoca
        self.view.log_action("Filtro P&B aplicado.")

    def apply_equalization(self):
        tk_main_image, tk_hist_image = self.model.equalize_histogram()
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)
        self.view.log_action("Equalização de histograma aplicada.")

    # reset_image: O "CTRL+Z" do app.
    # Pede ao Model pra jogar fora a imagem processada
    # e pegar a original de novo.
    # Também manda a View resetar os sliders.
    def reset_image(self):
        tk_main_image, tk_hist_image = self.model.reset_image()
        if tk_main_image:
            self.view.display_image_proc(tk_main_image)
            self.view.display_histogram(tk_hist_image)
            self.view.reset_sliders() # Reseta brilho/contraste
            self.view.log_action("Imagem restaurada")
        else:
            self.view.log_action("Nenhuma imagem para restaurar")

    #
    # O resto dos 'apply_...' são só mais do mesmo padrão.
    #
            
    def apply_rgb(self):
        tk_main_image, tk_hist_image = self.model.convert_to_rgb()
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)
        self.view.log_action("Conversão para RGB")

    def apply_rgba(self):
        tk_main_image, tk_hist_image = self.model.convert_to_rgba()
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)
        self.view.log_action("Conversão para RGBA")

    def apply_hsv(self):
        tk_main_image, tk_hist_image = self.model.convert_to_hsv()
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)
        self.view.log_action("Conversão para HSV")

    def apply_lab(self):
        tk_main_image, tk_hist_image = self.model.convert_to_lab()
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)
        self.view.log_action("Conversão para LAB")

    def apply_cmyk(self):
        tk_main_image, tk_hist_image = self.model.convert_to_cmyk()
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)
        self.view.log_action("Conversão para CMYK")

    def apply_otsu(self):
        tk_main, tk_hist = self.model.apply_otsu_threshold()
        if tk_main:
            self.view.display_image_proc(tk_main)
            self.view.display_histogram(tk_hist)
            self.view.log_action("Limiar de Otsu aplicado.")

    def apply_global_127(self):
        tk_main, tk_hist = self.model.apply_global_threshold(127)    
        if tk_main:
            self.view.display_image_proc(tk_main)
            self.view.display_histogram(tk_hist)
            self.view.log_action("Limiar Global (127) aplicado.")

    def apply_adaptive(self):
        tk_main, tk_hist = self.model.apply_adaptive_threshold()
        if tk_main:
            self.view.display_image_proc(tk_main)
            self.view.display_histogram(tk_hist)
            self.view.log_action("Limiar Adaptativo aplicado.")

    def apply_posterize_4(self):
        tk_main, tk_hist = self.model.apply_posterization(levels=4)    
        if tk_main:
            self.view.display_image_proc(tk_main)
            self.view.display_histogram(tk_hist)
            self.view.log_action("Posterização (4 Tons) aplicada.")

    # apply_global_adjustable: Um filtro 'apply' especial.
    # Em vez de só rodar, ele primeiro abre um POP-UP
    # pra perguntar o valor do limiar pro usuário.
    def apply_global_adjustable(self):
        if self.model.image is None:
            self.view.log_action("Nenhuma imagem carregada.")
            return

        # 1. Abre o pop-up e pega o número
        value = simpledialog.askinteger(
            "Limiar Global",                          # Título
            "Digite o valor do limiar (0-255):",      # Pergunta
            initialvalue=127,                       
            minvalue=0,                             
            maxvalue=255                            
        )
        
        # 2. Se o usuário deu OK (value não é None)...
        if value is not None:
            # 3. ...aplica o filtro usando o valor que ele digitou.
            tk_main, tk_hist = self.model.apply_global_threshold(threshold_value=value)
            
            if tk_main:
                self.view.display_image_proc(tk_main)
                self.view.display_histogram(tk_hist)
                self.view.log_action(f"Limiar Global ({value}) aplicado.")
            else:
                self.view.log_action(f"Erro ao aplicar Limiar Global ({value}).")