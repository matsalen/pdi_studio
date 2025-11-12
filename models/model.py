import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import io  # Input/Output

class Model:
    def __init__(self):
        self.image = None
        self.original = None

    def load_image(self, path):
        self.image = cv2.imread(path)
        self.original = self.image.copy()
        return self.to_tk_image(self.image)

    def save_image(self, path):
        if self.image is not None:
            cv2.imwrite(path, self.image)

    def reset_image(self):
        if self.original is not None:
            self.image = self.original.copy()
            return self._update_and_get_views(self.image, save_as_base=True)
        else:
            return None, None
        
    # --- NOVA FUNÇÃO DE LÓGICA ---
    
    def adjust_brightness_contrast(self, alpha, beta):
        """
        Aplica brilho/contraste lendo da "última imagem filtrada".
        NÃO salva isso como a nova base.
        """
        if self.last_filtered_image is None:
            return None, None
            
        # A MÁGICA:
        # cv2.convertScaleAbs(imagem, alpha=CONTRASTE, beta=BRILHO)
        adjusted_image = cv2.convertScaleAbs(self.last_filtered_image, alpha=alpha, beta=beta)
        
        # Chama o gatekeeper, mas NÃO salva como nova base
        return self._update_and_get_views(adjusted_image, save_as_base=False)

    # ========== Operações de PDI ==========
    def convert_to_gray(self):
        if self.image is None:
            return None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return self._update_and_get_views(self.image, save_as_base=True)

    def equalize_histogram(self):
        
        if self.image is None:
            return None, None

        # 1. Converte BGR -> HSV
        img_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        
        # 2. Separa os canais
        h, s, v = cv2.split(img_hsv)
        
        # 3. Equaliza APENAS o canal 'V' (Valor/Brilho)
        v_equalized = cv2.equalizeHist(v)
        
        # 4. Junta os canais (H e S originais + V novo)
        img_hsv_equalized = cv2.merge([h, s, v_equalized])
        
        # 5. Converte HSV -> BGR
        bgr_image = cv2.cvtColor(img_hsv_equalized, cv2.COLOR_HSV2BGR)
        
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    def convert_to_rgb(self):
        if self.image is None:
            return None
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        return self._update_and_get_views(self.image, save_as_base=True)
    
    def convert_to_rgba(self):
        if self.image is None:
            return None
        rgba = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)
        self.image = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
        return self._update_and_get_views(self.image, save_as_base=True)
    
    def convert_to_hsv(self):
        if self.image is None:
            return None
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return self._update_and_get_views(self.image, save_as_base=True)
    
    def convert_to_lab(self):
        if self.image is None:
            return None
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        self.image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return self._update_and_get_views(self.image, save_as_base=True)
    
    def convert_to_cmyk(self):
        if self.image is None:
            return None
        cmyk = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(cmyk)
        pil_cmyk = pil_img.convert('CMYK')
        pil_rgb = pil_cmyk.convert('RGB')
        numpy_rgb = np.array(pil_rgb)
        bgr_image = cv2.cvtColor(numpy_rgb, cv2.COLOR_RGB2BGR)

        return self._update_and_get_views(bgr_image, save_as_base=True)  
    
    def apply_otsu_threshold(self):
        if self.image is None: return None, None

        # 1. Converte para P&B
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # 2. Aplica o threshold de Otsu
        # O '0' é ignorado, pois o Otsu encontra o valor
        # O 'ret_val' será o limiar que o Otsu calculou (legal para logar!)
        ret_val, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 3. Converte de volta para BGR
        bgr_image = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
        
        # 4. Chama o gatekeeper
        # (O Controller pode logar o ret_val se quiser)
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    def apply_global_threshold(self, threshold_value=127):
        if self.image is None: return None, None

        # 1. Converte para P&B
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # 2. Aplica o threshold com o valor fixo
        ret, binary_img = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        
        # 3. Converte de volta para BGR
        bgr_image = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
        
        # 4. Chama o gatekeeper
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    def apply_adaptive_threshold(self):
        if self.image is None: return None, None

        # 1. Converte para P&B
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # 2. Aplica o threshold adaptativo (baseado na média da vizinhança)
        # 11 = Tamanho do bloco (bloco 11x11 pixels)
        # 2 = Constante C (subtraída da média)
        binary_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
        
        # 3. Converte de volta para BGR
        bgr_image = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
        
        # 4. Chama o gatekeeper
        return self._update_and_get_views(bgr_image, save_as_base=True)
    
    def apply_posterization(self, levels=4):
        """
        Reduz a imagem para 'levels' (níveis) de tons em P&B.
        (Ex: levels=2 é binarização, levels=4 são 4 tons de cinza)
        """
        if self.image is None: return None, None
        
        # 1. Converte para P&B
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # 2. Calcula o tamanho de cada "degrau"
        step = 256.0 / levels # Ex: 4 níveis -> step = 64.0
        
        # 3. Mapeia todos os pixels para o meio do degrau
        # (gray / step) -> Mapeia 0-255 para 0-4
        # np.floor(...) -> Arredonda para 0, 1, 2, 3
        # (...) * step -> Mapeia de volta (0, 64, 128, 192)
        # (...) + (step / 2) -> Pega o meio (32, 96, 160, 224)
        quantized = np.floor(gray / step) * step + (step / 2)
        
        # 4. Garante que o tipo de dado é 'uint8' (imagem)
        quantized_img = np.uint8(quantized)
        
        # 5. Converte de volta para BGR
        bgr_image = cv2.cvtColor(quantized_img, cv2.COLOR_GRAY2BGR)
        
        # 6. Chama o gatekeeper
        return self._update_and_get_views(bgr_image, save_as_base=True)

    def _update_and_get_views(self, new_bgr_image, save_as_base=True): # <-- MUDANÇA
        """
        Função 'gatekeeper' PRIVADA.
        """
        # 1. Salva a nova imagem como a imagem 'mestra'
        self.image = new_bgr_image 
        
        # 2. SALVA COMO BASE (só se for um filtro, não um slider)
        if save_as_base:
            self.last_filtered_image = new_bgr_image.copy()
        
        # 3. Gera a imagem principal para a View
        tk_main_image = self.to_tk_image(self.image)
        
        # 4. Gera a imagem do histograma para a View
        histogram_bgr_img = self.create_histogram_image(self.image)
        tk_hist_image = self.to_tk_image(histogram_bgr_img)
        
        # 5. Retorna AMBAS as imagens prontas
        return tk_main_image, tk_hist_image  

    # ========== Conversão ==========
    def to_tk_image(self, cv_image):
        rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        return ImageTk.PhotoImage(img)
    
    def create_histogram_image(self, image_para_analise):

        if image_para_analise is None:
            return None

        # 1. Crie uma "Figura" (o gráfico) com Matplotlib
        fig = plt.figure(figsize=(2.9, 2.4), dpi=100) 
        
        # 2. Verifique se a imagem é P&B ou Colorida
        if len(image_para_analise.shape) < 3:
            # É CINZA (1 canal)
            hist = cv2.calcHist([image_para_analise], [0], None, [256], [0, 256])
            plt.plot(hist, color='gray')
            plt.title("Histograma (Intensidade)")
        
        else:
            # É COLORIDA (3 canais - BGR)
            colors = ('b', 'g', 'r') # Cores do OpenCV
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image_para_analise], [i], None, [256], [0, 256])
                plt.plot(hist, color=color)
            plt.title("Histograma (BGR)")

        # Define os limites do gráfico
        plt.xlim([0, 256])
        plt.ylabel("Nº de Pixels")
        plt.xlabel("Intensidade")
        plt.tight_layout()

        # 3. Salve o gráfico em um buffer de memória
        buf = io.BytesIO()
        fig.savefig(buf, format='png') # <-- LINHA MODIFICADA
        buf.seek(0)

        # 4. Limpe o gráfico da memória do Matplotlib
        plt.close(fig)

        # 5. Abra a imagem do gráfico (que está no buffer) com o PIL
        pil_image = Image.open(buf)
        
        # Converte de RGBA (que o matplotlib salva) para RGB
        if pil_image.mode == 'RGBA':
             pil_image = pil_image.convert('RGB')
             
        numpy_rgb = np.array(pil_image)
        numpy_bgr = cv2.cvtColor(numpy_rgb, cv2.COLOR_RGB2BGR)

        return numpy_bgr
