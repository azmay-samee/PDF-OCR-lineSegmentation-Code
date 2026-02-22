import cv2
import numpy as np
from skimage import img_as_ubyte
from skimage.filters import threshold_sauvola
import os

class ImageProcessor:
    def __init__(self):
        self.original = None
        self.gray = None
        self.binary = None

    def __ReadImage__(self, path, grayed=False):
        if grayed:
            self.gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        else:
            self.original = cv2.imread(path)
            if self.original is None:
                raise ValueError(f"Image not found at path: {path}")

    def to_grayscale(self):
        self.gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        return self.gray

    # def sauvola_binarize(self, window_size=25, k=0.2):
    #     sauvola_thresh = threshold_sauvola(self.gray, window_size=window_size, k=k)
    #     self.binary = img_as_ubyte(self.gray > sauvola_thresh)
    #     return self.binary
    def sauvola_binarize(self, window_size=25, k=0.2):
        sauvola_thresh = threshold_sauvola(self.gray, window_size=window_size, k=k)
        self.binary = img_as_ubyte(self.gray > sauvola_thresh)
        return self.binary

    def writeImg(self, path, name, img):
        if img is None:
            raise ValueError("Image is empty or not loaded.")
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, name)
        ext = os.path.splitext(full_path)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            raise ValueError(f"Invalid image extension: '{ext}'")
        if os.path.exists(full_path):
            print(f"Skipped writing duplicate: {full_path}")
        else:
            print(f"Saving to: {full_path}, Image shape: {img.shape}, dtype: {img.dtype}")
            cv2.imwrite(full_path, img)
