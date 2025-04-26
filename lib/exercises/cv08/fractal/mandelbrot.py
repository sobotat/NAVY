from lib.exercises.cv08.fractal.fractal import Fractal
import numpy as np
from PIL import Image, ImageTk
import colorsys
from tqdm import tqdm
from multiprocessing import Pool

class MandelbrotSet(Fractal):
    def __init__(self, width, height, max_iter=100):
        super().__init__(width, height, max_iter)
        self.x_min = -2.0
        self.x_max = 1.0
        self.y_min = -1.0
        self.y_max = 1.0
        self.compute()

    def compute(self):
        re = np.linspace(self.x_min, self.x_max, self.width)
        im = np.linspace(self.y_min, self.y_max, self.height)

        img_array = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        for i in tqdm(range(self.width), "Computing"):
            for j in range(self.height):
                c = complex(re[i], im[j])
                z = complex(0, 0)
                iteration = 0

                while abs(z) <= 2 and iteration < self.max_iter:
                    z = (z ** 2) + c
                    iteration += 1

                if iteration < self.max_iter:
                    hue = iteration / self.max_iter
                    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1.0 if iteration < self.max_iter else 0)
                    img_array[j, i] = (int(r * 255), int(g * 255), int(b * 255))

        self.image = ImageTk.PhotoImage(Image.fromarray(img_array))