import numpy as np
from PIL import Image
from numba import jit
import random
from numba import jit

width=1440
height=900

@jit
def above(a,b,x,y):
    return ((a*x+b)>y)

@jit
def generate(w,h):
    data=np.zeros((width,height),np.uint8)
    diff=1
    for i in range(200):
        a=(random.random()-.5)*2
        b=random.randint(0,height)-round(height/2)
        f=random.randint(0,1)
        for x in range(width):
            for y in range(height):
                if above(a,height/2-b,x-round(width/2),y):
                    data[x,y]+=diff
                else:
                    data[x,y]-=diff
                data[x,y]*=0.9999
    return data


data=[]
data=generate(width,height)[:]
img=Image.fromarray(data.T,"L")                
img.save("/Users/kazamatzuri/projects/wallpapergen/random.png")