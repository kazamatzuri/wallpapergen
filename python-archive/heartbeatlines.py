#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image
from geomdl import BSpline, knotvector
from operator import add, sub
from random import randint, random, seed
from numpy import pi
from numpy import sin
from numba import jit
import numpy as np

WIDTH = 1440 * 4
HEIGHT = 900 * 4


# In[88]:


def linespread():
    return [[x, HEIGHT / 2] for x in range(0, WIDTH, 90)]


@jit
def splinei():
    curve = BSpline.Curve()
    curve.degree = 3
    curve.delta = 0.000005
    lpoints = linespread()
    curve.ctrlpts = lpoints
    curve.knotvector = knotvector.generate(3, len(curve.ctrlpts))
    curve_points = curve.evalpts
    yield curve_points
    while True:
        for p in lpoints:
            p[1] += int((random() - 0.5) * (25) * (sin((p[0]) * (pi / WIDTH)) ** 2))
            p[0] += int((random() - 0.5) * (5) * (sin((p[0]) * (pi / WIDTH)) ** 2))
        curve.ctrlpts = lpoints
        curve_points = curve.evalpts
        yield curve_points


# In[89]:


@jit
def splinetest(pixels):
    splineit = splinei()
    decay = 0.91
    color = 255
    depth = 1500
    for s in range(depth):
        color = 1  # (s*2)+49
        p = next(splineit)
        for sp in p:
            x = int(sp[0])
            y = int(sp[1])
            if (x >= 0) and (x < WIDTH) and (y >= 0) and (y < HEIGHT):
                c = pixels[x, y]
                # newc=tuple(map(sub,c,(int(color),int(color),int(color),1)))
                newc = c - (255 / depth)
                # print(newc)
                pixels[x, y] = newc


# In[ ]:

img = Image.new("RGBA", (WIDTH, HEIGHT), "white")  # create a new black image
pixels = img.load()  # create the pixel map
seed()

temppixels = np.full((WIDTH, HEIGHT), 255.0)
splinetest(temppixels)
for x in range(WIDTH):
    for y in range(HEIGHT):
        pixels[x, y] = (
            int(temppixels[x, y]),
            int(temppixels[x, y]),
            int(temppixels[x, y]),
            255,
        )
img.save("/tmp/test.png")


# In[ ]:
