#!/usr/bin/env python
# coding: utf-8

# In[82]:


from PIL import Image
from geomdl import BSpline,knotvector
from operator import add,sub
from random import randint,random,seed
from numpy import pi
from numpy import sin
WIDTH=1440
HEIGHT=900
# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]



# In[78]:


def splinei(it=30):
    curve = BSpline.Curve()
    curve.degree = 3
    curve.delta=0.0001
    lpoints=[[x,HEIGHT/2] for x in range(0,WIDTH,40)]
    curve.ctrlpts=lpoints
    curve.knotvector = knotvector.generate(3,len(curve.ctrlpts))
    curve_points=curve.evalpts
    yield curve_points
    for iter in range(it):
        for p in lpoints:
            p[1]+=int((random()-0.5)*(60)*sin((p[0])*(pi/WIDTH)))
            p[0]+=int((random()-0.5)*(20)*sin((p[0])*(pi/WIDTH)))
        curve.ctrlpts=lpoints
        curve_points=curve.evalpts
        yield curve_points


# In[88]:


def splinetest(pixels):
    splineit=splinei(500)
    decay=.91
    color=255
    for s in range(100):
        color*=decay
        p = next(splineit)
        for sp in p:
            x=int(sp[0])
            y=int(sp[1])
            if (x>=0) and (x<WIDTH) and (y>=0) and (y<HEIGHT):
                c=pixels[x,y]
                newc=tuple(map(sub,c,(int(color),int(color),int(color),1)))
                #print(newc)
                pixels[x,y]=newc
                
    


# In[90]:


img = Image.new( 'RGBA', (WIDTH,HEIGHT), "white") # create a new black image
pixels = img.load() # create the pixel map
seed()
splinetest(pixels)
img.show()


# In[ ]:




