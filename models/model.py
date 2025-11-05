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
            return self._update_and_get_views(self.image)
        else:
            return None, None

    # ========== Operações de PDI ==========
    def convert_to_gray(self):
        if self.image is None:
            return None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return self._update_and_get_views(self.image)

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
        
        return self._update_and_get_views(bgr_image)
    
    def convert_to_rgb(self):
        if self.image is None:
            return None
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        return self._update_and_get_views(self.image)
    
    def convert_to_rgba(self):
        if self.image is None:
            return None
        rgba = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)
        self.image = cv2.cvtColor(rgba, cv2.COLOR_BGRA2BGR)
        return self._update_and_get_views(self.image)
    
    def convert_to_hsv(self):
        if self.image is None:
            return None
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return self._update_and_get_views(self.image)
    
    def convert_to_lab(self):
        if self.image is None:
            return None
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        self.image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return self._update_and_get_views(self.image)
    
    def convert_to_cmyk(self):
        if self.image is None:
            return None
        cmyk = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(cmyk)
        pil_cmyk = pil_img.convert('CMYK')
        pil_rgb = pil_cmyk.convert('RGB')
        numpy_rgb = np.array(pil_rgb)
        bgr_image = cv2.cvtColor(numpy_rgb, cv2.COLOR_RGB2BGR)

        return self._update_and_get_views(bgr_image)  

    def _update_and_get_views(self, new_bgr_image):

        # 1. Salva a nova imagem como a imagem 'mestra'
        self.image = new_bgr_image 
        
        # 2. Gera a imagem principal para a View
        tk_main_image = self.to_tk_image(self.image)
        
        # 3. Gera a imagem do histograma para a View
        histogram_bgr_img = self.create_histogram_image(self.image)
        tk_hist_image = self.to_tk_image(histogram_bgr_img)
        
        # 4. Retorna AMBAS as imagens prontas
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
