#!/usr/bin/env python
# coding: utf-8

##
# We start with this idea:
# create a spline based on a few anchor points
# along this line we spread a fixed amount of color between a random amount of pixels
# (think of a drop of paint(fixed amount) spread out over a random area)
# in this case the area is perpendicular to the current slope of the spline
#
# now, over time (iterations) we wiggle a bit on the anchor points of the spline, so the
# line changes shape over each iteration

from PIL import Image
from geomdl import BSpline, knotvector
from operator import add, sub
from random import randint, random, seed
from numpy import pi
from numpy import sin
from numba import jit
import numpy as np
import math

WIDTH = 1440
HEIGHT = 900


def linespread():
    # initializes the anchor points.
    # the third coordinate is being used for thickness of the spread of color
    # we want that part of the spline it's smooth
    return [
        [x, HEIGHT / 2, ((random() - 0.5) * (40) * (sin((x) * (pi / WIDTH))))]
        for x in range(0, WIDTH, 90)
    ]


@jit
def splinei():
    curve = BSpline.Curve()
    curve.degree = 3
    curve.delta = 0.00005
    lpoints = linespread()
    curve.ctrlpts = lpoints
    curve.knotvector = knotvector.generate(3, len(curve.ctrlpts))
    curve_points = curve.evalpts
    yield curve_points
    while True:
        for p in lpoints:
            p[1] += int((random() - 0.5) * (25) * (sin((p[0]) * (pi / WIDTH)) ** 2))
            p[0] += int((random() - 0.5) * (5) * (sin((p[0]) * (pi / WIDTH)) ** 2))
            p[2] += int((random() - 0.5) * (10) * (sin((p[0]) * (pi / WIDTH)) ** 2))
        curve.ctrlpts = lpoints
        curve_points = curve.evalpts
        yield curve_points


# In[89]:


@jit
def splinetest(pixels):
    splineit = splinei()
    decay = 0.91
    color = 255
    # we draw <depth> steps of the splineiterator
    depth = 300
    # bucket is the amount of color that gets spread out in <grains> (determine randomly)
    bucket = 1.0
    for s in range(depth):
        color = 1  # (s*2)+49
        p = next(splineit)
        for i in range(1, len(p)):
            sp = p[i]
            lp = p[i - 1]
            px, py = lp[0], lp[1]
            x = sp[0]
            y = sp[1]
            s = sp[2]
            if (x - px) != 0:
                grains = randint(5, 20)
                for g in range(grains):
                    # random spread of grains
                    loc = (random() - 0.5) * s
                    # perpendicular to the current slope of the spline
                    # calculated here
                    length = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                    dx = -(y - py) / length
                    dy = (x - px) / length
                    # dx,dy is the normalized 90 degree angle(to the slope) vector

                    tx = x + loc * dx
                    ty = y + loc * dy
                    # tx,ty are now the location of where the grain falls along that vector

                    # avoid oob errors
                    if (tx >= 0) and (tx < WIDTH) and (ty >= 0) and (ty < HEIGHT):
                        c = pixels[int(tx), int(ty)]
                        # c is previous color, now substract the new value from the current one
                        # note, we are working with a white base img and only in greyscale so far
                        newc = c - (bucket / grains)
                        if newc < 0:
                            newc = 0
                        # print(newc)
                        pixels[int(tx), int(ty)] = newc



img = Image.new("RGBA", (WIDTH, HEIGHT), "white")  # create a new white image
pixels = img.load()  # create the pixel map
seed()

# we use temppixels, because to get nice results we need to do the color calc in float
# not in ints....
temppixels = np.full((WIDTH, HEIGHT), 255.0)
splinetest(temppixels)
# map the temp pixels back into the image
# note: no list comprehension since pixels isn't a list (maybe there is a way to cast it, but I haven't found it yet)
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
