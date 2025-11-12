from tkinter import Tk, filedialog, messagebox
from models.model import Model
from views.view import View

class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.title("PDI Studio - Sistema Interativo de Processamento de Imagens")
        self.root.geometry("1600x900")

        # Model
        self.model = Model()

        # View
        self.view = View(self.root, controller=self)

        self.view.contrast_slider.config(command=self.on_slider_move)
        self.view.brightness_slider.config(command=self.on_slider_move)

    # ========== Métodos principais ==========
    def run(self):
        self.root.mainloop()

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if path:
            image = self.model.load_image(path)
            self.view.display_image(image)
            self.view.reset_sliders() # <-- NOVO
            # O reset_image já está sendo chamado pelo 'apply_gray' etc.,
            # então o histograma inicial já deve estar certo
            # Mas vamos forçar uma atualização inicial
            self.apply_gray() # Chama um filtro qualquer pra popular a direita
            self.reset_image() # E reseta pra ficar igual
            self.view.log_action(f"Imagem carregada: {path}")

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

    def on_slider_move(self, value):
        """ Chamado sempre que *qualquer* slider for movido. """
        
        # Não sobrecarregue o log
        # self.view.log_action("Ajustando brilho/contraste...") 
        
        if self.model.image is None:
            return

        try:
            # 1. Pega os valores ATUAIS de AMBOS os sliders
            alpha = self.view.contrast_slider.get() # Contraste
            beta = self.view.brightness_slider.get()  # Brilho
            
            # 2. Chama a nova função do Model
            tk_main, tk_hist = self.model.adjust_brightness_contrast(alpha, beta)
            
            # 3. Atualiza a View (sem spammar o log)
            if tk_main:
                self.view.display_image_proc(tk_main)
                self.view.display_histogram(tk_hist)
                
        except Exception as e:
            # É melhor não logar aqui, senão vai spammar muito
            pass
    
    

    def apply_gray(self):
        tk_main_image, tk_hist_image = self.model.convert_to_gray()
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)        
        self.view.log_action("Filtro P&B aplicado.")

    def apply_equalization(self):
        tk_main_image, tk_hist_image = self.model.equalize_histogram()
        self.view.display_image_proc(tk_main_image)
        self.view.display_histogram(tk_hist_image)
        self.view.log_action("Equalização de histograma aplicada.")

    def reset_image(self):
        tk_main_image, tk_hist_image = self.model.reset_image()
        if tk_main_image:
            self.view.display_image_proc(tk_main_image)
            self.view.display_histogram(tk_hist_image)
            self.view.reset_sliders() # <-- NOVO
            self.view.log_action("Imagem restaurada")
        else:
            self.view.log_action("Nenhuma imagem para restaurar")

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
        # Passando o valor 127
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
        # Passando o número de níveis
        tk_main, tk_hist = self.model.apply_posterization(levels=4) 
        if tk_main:
            self.view.display_image_proc(tk_main)
            self.view.display_histogram(tk_hist)
            self.view.log_action("Posterização (4 Tons) aplicada.")