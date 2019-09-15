from random import randint
from random import random
import math
import numpy as np
from numba import jit


class SpreadLines:
    def __init__(self, pixels,bucket=255.0):
        #self.points = curve_points
        self.img_data = pixels
        self.bucket=bucket

    @jit
    def drawline(self,curve_points):
        maxc=0.0
        for i in range(1, len(curve_points)):
            #if (i%100==0):
                #print("point: "+str(i))
            WIDTH=self.img_data.shape[0]
            HEIGHT=self.img_data.shape[1]
            sp = curve_points[i]
            lp = curve_points[i - 1]
            px, py = lp[0], lp[1]
            x = sp[0]
            y = sp[1]
            s = sp[2]            
            if (x - px) != 0:
                length = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                dx = -(y - py) / length
                dy = (x - px) / length               
                #going to spread <bucket> amount of color
                tx1,ty1 = x + s * dx,y + s * dy
                tx2,ty2 = x - s * dx,y - s * dy
                num=int(math.sqrt((tx1-tx2)**2+(ty1-ty2)**2)/0.1)
                if num==0:
                    num=1
                color_gradient=self.bucket/num
                xr=np.linspace(tx1,tx2,num)
                yr=np.linspace(ty1,ty2,num)
                for i in range(num-1):
                    tx,ty=xr[i],yr[i]
                    # avoid oob errors
                    if (tx >= 0) and (tx < WIDTH) and (ty >= 0) and (ty < HEIGHT):
                        c = self.img_data[int(tx), int(ty)]
                        newc = c + color_gradient
                        if newc > maxc:
                            maxc=newc
                        # print(newc)
                        self.img_data[int(tx), int(ty)] = newc
        return maxc
