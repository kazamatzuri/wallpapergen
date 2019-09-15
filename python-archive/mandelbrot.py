import numpy as np
from PIL import Image
from numba import jit


@jit
def mandelbrot(creal, cimag, maxiter):
    real = creal
    imag = cimag
    for n in range(maxiter):
        real2 = real * real
        imag2 = imag * imag
        if real2 + imag2 > 4.0:
            return n
        imag = 2 * real * imag + cimag
        real = real2 - imag2 + creal
    return 0


@jit
def graph(xmin, xmax, ymin, ymax, width, height, maxiter):
    data = np.zeros((width, height), np.uint8)
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    for i in range(width):
        for j in range(height):
            data[i, j] = mandelbrot(r1[i], r2[j], maxiter)
    img = Image.fromarray(data.T, "L")
    return img


X = 0.281717921930775
Y = 0.5771052841488505
R = 4.75e-13
img = graph(X - R, X + R, Y - R, Y + R, 2880, 1800, 5000)
img.save("mandelbrot/wallpaper.png")
