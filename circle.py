import numpy as np
from numpy import pi
from numpy import array
from numpy.random import random
from numpy.random import randint

from numpy import linspace
from numpy import arange
from numpy import column_stack
from numpy import cos
from numpy import sin
from PIL import Image,ImageOps
from geomdl import BSpline,knotvector


SIZE=2000
R=800
TWOPI=2*pi
WOBBLE=250
DECAYLENGTH=50
crange=np.linspace(65535,200,DECAYLENGTH)

def draw(size):
    data=[]
    data=np.ones((size,size),np.uint16)*65535
    for _ in range(2):
        pnum = randint(15,100)
        a = random()*TWOPI + linspace(0, TWOPI, pnum)
        points = column_stack((cos(a), sin(a))) * (1500+random()*100)
        curve = BSpline.Curve()
        curve.degree = 3
        #lpoints=list(list([i[0]+randint(-WOBBLE,WOBBLE),i[1]+randint(-WOBBLE,WOBBLE)]) for i in points)
        #curve.ctrlpts=lpoints
        #print(curve.ctrlpts)
        
       
        curve.delta=0.00001
        #curve_points=curve.evalpts
#         for t in curve_points:
#             data[int(round(t[0]+size/2)),int(round(t[1]+size/2))]=65535
            #print(int(round(t[0]+size/2)),int(round(t[1]+size/2)))
        
        for decay in range(DECAYLENGTH):
                #print(crange[decay])
                lpoints=list(list([i[0]+randint(-WOBBLE,WOBBLE),i[1]+randint(-WOBBLE,WOBBLE)]) for i in points)
                curve.ctrlpts=lpoints
                curve.knotvector = knotvector.generate(3,len(curve.ctrlpts))
                curve_points=curve.evalpts
                for t in curve_points:
                    data[int(round(t[0]+size/2)),int(round(t[1]+size/2))]+=int(crange[decay])
                                                                           
    return data

data = draw(5000)
array_buffer = data.T.tobytes()
img = Image.new("I", data.shape)
img.frombytes(array_buffer, 'raw', "I;16")
img=img.resize((1000,1000),Image.ANTIALIAS)
#img=ImageOps.invert(img)
img.save("circle.png")
#img.show()