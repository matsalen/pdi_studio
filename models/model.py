import cv2
from PIL import Image, ImageTk
import numpy as np

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
            return self.to_tk_image(self.image)

    # ========== Operações de PDI ==========
    def convert_to_gray(self):
        if self.image is None:
            return None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def equalize_histogram(self):
        if self.image is None:
            return None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        self.image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)
    
    def convert_to_rgb(self):
        if self.image is None:
            return None
        pixel_bgr = self.image[100, 100]
        print(f"Pixel BGR original: {pixel_bgr}")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pixel_pro = gray[100, 100]
        print(f"Pixel processado convertido: {pixel_pro}")
        self.image = cv2.cvtColor(gray, cv2.COLOR_RGB2BGR)
        return self.to_tk_image(self.image)
    
    def convert_to_rgba(self):
        if self.image is None:
            return None
        pixel_bgr = self.image[100, 100]
        print(f"Pixel BGR original: {pixel_bgr}")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)
        pixel_pro = gray[100, 100]
        print(f"Pixel processado convertido: {pixel_pro}")
        self.image = cv2.cvtColor(gray, cv2.COLOR_BGRA2BGR)
        return self.to_tk_image(self.image)
    
    def convert_to_hsv(self):
        if self.image is None:
            return None
        pixel_bgr = self.image[100, 100]
        print(f"Pixel BGR original: {pixel_bgr}")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        pixel_pro = gray[100, 100]
        print(f"Pixel processado convertido: {pixel_pro}")
        self.image = cv2.cvtColor(gray, cv2.COLOR_HSV2BGR)
        return self.to_tk_image(self.image)
    
    def convert_to_lab(self):
        if self.image is None:
            return None
        pixel_bgr = self.image[100, 100]
        print(f"Pixel BGR original: {pixel_bgr}")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        pixel_pro = gray[100, 100]
        print(f"Pixel processado convertido: {pixel_pro}")
        self.image = cv2.cvtColor(gray, cv2.COLOR_LAB2BGR)
        return self.to_tk_image(self.image)
    
    def convert_to_cmyk(self):
        if self.image is None:
            return None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(gray)
        pil_cmyk = pil_img.convert('CMYK')
        pil_rgb = pil_cmyk.convert('RGB')
        print(f"Modo de cor (Mode): {pil_cmyk.mode}")
        print(f"Número de canais (Bands): {len(pil_cmyk.getbands())}")
        print(f"Tipo de objeto: {type(pil_cmyk)}")
        return ImageTk.PhotoImage(pil_rgb)

    # ========== Conversão ==========
    def to_tk_image(self, cv_image):
        rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        return ImageTk.PhotoImage(img)
