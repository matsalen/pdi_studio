import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import io  # Input/Output, pra gambiarra do gráfico

class Model:
    def __init__(self):
        # self.image é a foto da DIREITA (a que a gente zoa)
        self.image = None
        # self.original é a foto da ESQUERDA (a intocada, o backup)
        self.original = None
        # self.last_filtered_image é a "base" pros sliders.
        # Se você aplica "Tons de Cinza", essa foto vira a base.
        # Os sliders de brilho vão mexer na foto em *tons de cinza*.
        self.last_filtered_image = None

    def load_image(self, path):
        # Lê a imagem do HD
        self.image = cv2.imread(path)
        # Faz a cópia de segurança
        self.original = self.image.copy()
        # A primeira "base" pros sliders é a própria imagem
        self.last_filtered_image = self.image.copy()
        
        # Devolve a imagem 'tk' pra View (pro painel da ESQUERDA)
        return self.to_tk_image(self.image)

    def save_image(self, path):
        # Salva a imagem zoada (self.image) no HD
        if self.image is not None:
            cv2.imwrite(path, self.image)

    def reset_image(self):
        # O "CTRL+Z". Joga fora a imagem zoada...
        if self.original is not None:
            # ...e pega a cópia de segurança de volta.
            self.image = self.original.copy()
            # Manda o 'portão' atualizar tudo (e salvar como nova base)
            return self._update_and_get_views(self.image, save_as_base=True)
        else:
            return None, None
            
    # adjust_brightness_contrast: A mágica dos sliders.
    # alpha = Contraste, beta = Brilho
    def adjust_brightness_contrast(self, alpha, beta):
        # Se não tiver uma "base" pra mexer, não faz nada.
        if self.last_filtered_image is None:
            return None, None
            
        # A matemática do brilho/contraste.
        # O importante: ele lê da 'base' (last_filtered_image),
        # e não da 'self.image' (que foi o resultado do slider *anterior*).
        # Isso impede o efeito de "empilhar".
        adjusted_image = cv2.convertScaleAbs(self.last_filtered_image, alpha=alpha, beta=beta)
        
        # Chama o 'portão', mas com 'save_as_base=False'.
        # Isso aqui é SÓ UMA PRÉVIA. Não salva como a nova base.
        return self._update_and_get_views(adjusted_image, save_as_base=False)

    # -----------------------------------------------------------------
    # O PADRÃO DOS FILTROS (Tudo abaixo)
    # 1. Faz a matemática (cv2.cvtColor, cv2.threshold, etc.).
    # 2. Garante que o resultado final seja BGR (pra manter o padrão).
    # 3. Chama o 'portão' _update_and_get_views,
    #    passando a nova imagem e 'save_as_base=True'.
    # -----------------------------------------------------------------

    def convert_to_gray(self):
        if self.image is None:
            return None, None # (o 'None, None' é pra tupla que o Controller espera)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # Converte DE VOLTA pra BGR. É, eu sei, parece burro.
        # Mas é pra manter os 3 canais e o resto do código (hist, save) feliz.
        bgr_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return self._update_and_get_views(bgr_image, save_as_base=True)

    # equalize_histogram: O "photoshop automático"
    def equalize_histogram(self):
        if self.image is None:
            return None, None

        # Pra não zoar as cores, a gente NUNCA equaliza BGR.
        # 1. Converte BGR -> HSV (Matiz, Saturação, BRILHO)
        img_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        
        # 2. Separa os canais
        h, s, v = cv2.split(img_hsv)
        
        # 3. Equaliza SÓ o canal 'V' (Brilho)
        v_equalized = cv2.equalizeHist(v)
        
        # 4. Junta de volta (cores originais + brilho novo)
        img_hsv_equalized = cv2.merge([h, s, v_equalized])
        
        # 5. Converte HSV -> BGR
        bgr_image = cv2.cvtColor(img_hsv_equalized, cv2.COLOR_HSV2BGR)
        
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    # O resto das conversões são "bate-e-volta".
    # Elas convertem (ex: BGR->HSV) e convertem de volta (HSV->BGR).
    # O resultado é uma imagem BGR que "parece" HSV,
    # mostrando os canais de forma bizarra. É pra teste visual.
    
    def convert_to_rgb(self):
        if self.image is None: return None, None
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        bgr_image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR) # Sim, BGR->RGB->BGR. Não faz nada.
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    def convert_to_rgba(self):
        if self.image is None: return None, None
        rgba = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)
        bgr_image = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR) # BGR->BGRA->BGR. Perde o Alfa.
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    def convert_to_hsv(self):
        if self.image is None: return None, None
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        bgr_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) # BGR->HSV->BGR (Pode perder cor)
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    def convert_to_lab(self):
        if self.image is None: return None, None
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        bgr_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR) # BGR->LAB->BGR (Pode perder cor)
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    # CMYK é o chatinho que precisa do PIL (Pillow) no meio
    def convert_to_cmyk(self):
        if self.image is None: return None, None
        
        # 1. OpenCV (BGR) -> OpenCV (RGB)
        cmyk_step1 = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # 2. OpenCV (RGB) -> PIL (RGB)
        pil_img = Image.fromarray(cmyk_step1)
        # 3. PIL (RGB) -> PIL (CMYK)
        pil_cmyk = pil_img.convert('CMYK')
        # 4. PIL (CMYK) -> PIL (RGB) (pra poder ver na tela)
        pil_rgb = pil_cmyk.convert('RGB')
        # 5. PIL (RGB) -> Numpy/OpenCV (RGB)
        numpy_rgb = np.array(pil_rgb)
        # 6. OpenCV (RGB) -> OpenCV (BGR) (pro nosso padrão)
        bgr_image = cv2.cvtColor(numpy_rgb, cv2.COLOR_RGB2BGR)

        return self._update_and_get_views(bgr_image, save_as_base=True)  

    # apply_otsu_threshold: O limiar "automágico".
    # Ele acha o melhor valor pra separar "fundo" de "frente".
    def apply_otsu_threshold(self):
        if self.image is None: return None, None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # O '0' é só um placeholder, o OTSU acha o valor certo.
        ret_val, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        bgr_image = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    # apply_global_threshold: O limiar "burro".
    # Você manda o valor (ex: 127) e ele corta ali.
    def apply_global_threshold(self, threshold_value=127):
        if self.image is None: return None, None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        ret, binary_img = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        
        bgr_image = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    # apply_adaptive_threshold: O limiar "esperto" (parece um desenho).
    # Ele não usa UM valor, mas calcula o limiar pra CADA "vizinhança".
    def apply_adaptive_threshold(self):
        if self.image is None: return None, None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Bloco de 11x11, C=2 (ajustes finos)
        binary_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY, 11, 2)
        
        bgr_image = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    # apply_posterization: O "multi-tons".
    # Reduz de 256 tons de cinza para 'levels' (ex: 4 tons).
    def apply_posterization(self, levels=4):
        if self.image is None: return None, None
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Matemática chata pra "empilhar" os pixels em 'levels' degraus.
        step = 256.0 / levels
        quantized = np.floor(gray / step) * step + (step / 2)
        quantized_img = np.uint8(quantized)
        
        bgr_image = cv2.cvtColor(quantized_img, cv2.COLOR_GRAY2BGR)
        return self._update_and_get_views(bgr_image, save_as_base=True)

    # _update_and_get_views: O "PORTÃO".
    # O coração do Model. TODO filtro DESTRUTIVO (quase todos)
    # termina chamando essa função.
    def _update_and_get_views(self, new_bgr_image, save_as_base=True):
        
        # 1. Atualiza a imagem principal (da direita)
        self.image = new_bgr_image 
        
        # 2. Se for um filtro (não um slider), salva como a nova "base".
        if save_as_base:
            self.last_filtered_image = new_bgr_image.copy()
        
        # 3. Gera a imagem 'Tk' pra View (painel da direita)
        tk_main_image = self.to_tk_image(self.image)
        
        # 4. Gera o GRÁFICO do histograma (como imagem 'Tk')
        histogram_bgr_img = self.create_histogram_image(self.image)
        tk_hist_image = self.to_tk_image(histogram_bgr_img)
        
        # 5. Devolve os DOIS (imagem + gráfico) pro Controller
        return tk_main_image, tk_hist_image  

    # to_tk_image: O "Tradutor".
    # Converte a imagem do OpenCV (BGR) pra algo que o Tkinter entende (PhotoImage).
    def to_tk_image(self, cv_image):
        if cv_image is None:
            return None
        # BGR (OpenCV) -> RGB (OpenCV)
        rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        # RGB (OpenCV) -> Imagem PIL
        img = Image.fromarray(rgb)
        # Imagem PIL -> PhotoImage (Tkinter)
        return ImageTk.PhotoImage(img)
    
    # create_histogram_image: A "Gambiarra Oficial"
    # O Matplotlib (que desenha o gráfico) não fala com o Tkinter (pra imagem).
    # Então a gente...
    def create_histogram_image(self, image_para_analise):
        if image_para_analise is None:
            return None

        # 1. Manda o Matplotlib desenhar o gráfico (pequeno)
        fig = plt.figure(figsize=(2.9, 2.4), dpi=100) 
        
        # Se for P&B (1 canal), desenha 1 linha
        if len(image_para_analise.shape) < 3 or (image_para_analise[:,:,0] == image_para_analise[:,:,1]).all():
            hist = cv2.calcHist([image_para_analise], [0], None, [256], [0, 256])
            plt.plot(hist, color='gray')
            plt.title("Histograma (Intensidade)")
        
        # Se for Colorido (3 canais), desenha 3 linhas (B, G, R)
        else:
            colors = ('b', 'g', 'r')
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image_para_analise], [i], None, [256], [0, 256])
                plt.plot(hist, color=color)
            plt.title("Histograma (BGR)")

        plt.xlim([0, 256])
        plt.ylabel("Nº de Pixels")
        plt.xlabel("Intensidade")
        plt.tight_layout() # Pra não cortar os rótulos

        # 2. Salva esse gráfico como um "arquivo PNG na memória"
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        # 3. Limpa o Matplotlib (pra não vazar memória)
        plt.close(fig)

        # 4. Abre esse "PNG da memória" com o PIL
        pil_image = Image.open(buf)
        
        # 5. Converte o gráfico (RGBA) pra RGB
        if pil_image.mode == 'RGBA':
             pil_image = pil_image.convert('RGB')
             
        # 6. Converte o gráfico (RGB) pra BGR (pra nosso 'to_tk_image' usar)
        numpy_rgb = np.array(pil_image)
        numpy_bgr = cv2.cvtColor(numpy_rgb, cv2.COLOR_RGB2BGR)

        # 7. Retorna a IMAGEM DO GRÁFICO (em BGR)
        return numpy_bgr