import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from numba import jit

@jit(nopython=True)
def mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    mandelbrot_image = np.zeros((height, width), dtype=np.int32)

    for i in range(height):
        for j in range(width):
            c = complex(x[j], y[i])
            z = 0.0j
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            mandelbrot_image[i, j] = n

    return mandelbrot_image

class MandelbrotSet:
    def __init__(self, width=800, height=800, max_iter=256):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.pi_factor = np.pi
        self.current_zoom = 1.0
        self.zoom_factor = 1.1

        
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.slider = self.create_slider()
        self.plot_mandelbrot()

        
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('close_event', self.on_close)

    def create_slider(self):
        ax_slider = plt.axes([0.1, 0.01, 0.8, 0.03], facecolor='lightgoldenrodyellow')
        slider = Slider(ax_slider, 'Pi Factor', np.pi, 3 * np.pi, valinit=np.pi, valstep=0.01)
        slider.on_changed(self.update)
        return slider

    def plot_mandelbrot(self):
        x_min, x_max, y_min, y_max = self.get_plot_bounds()
        mandelbrot_image = mandelbrot_set(x_min, x_max, y_min, y_max, self.width, self.height, self.max_iter)

        self.ax.clear()
        self.ax.imshow(mandelbrot_image, cmap='hot', extent=(x_min, x_max, y_min, y_max))
        self.ax.set_title(f"Mandelbrot Set (zoom adjusted by π factor: {self.pi_factor:.2f})")
        plt.draw()

    def get_plot_bounds(self):
        zoom_level = self.pi_factor / np.pi
        x_min = -2.0 / zoom_level
        x_max = 1.0 / zoom_level
        y_min = -1.5 / zoom_level
        y_max = 1.5 / zoom_level
        return x_min, x_max, y_min, y_max

    def update(self, val):
        self.pi_factor = self.slider.val
        max_iter_dynamic = min(int(self.max_iter * (self.pi_factor / np.pi)), 1000)
        self.max_iter = max_iter_dynamic
        self.plot_mandelbrot()

    def on_scroll(self, event):
        if event.key == 'control':
            if event.button == 'up':
                self.current_zoom *= self.zoom_factor
            elif event.button == 'down':
                self.current_zoom /= self.zoom_factor
            self.pi_factor = np.pi * self.current_zoom
            self.slider.set_val(self.pi_factor)
            self.update(self.pi_factor)

    def on_close(self, event):
        plt.close(self.fig)

if __name__ == "__main__":
    try:
        MandelbrotSet()
        plt.show()
    except KeyboardInterrupt:
        print("Execution interrupted by user.")