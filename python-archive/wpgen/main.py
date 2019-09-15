import os, sys
import argparse
from random import seed
import logging
from PIL import Image
import numpy as np
from spreadlines.spreadlines import SpreadLines
from geomdl import BSpline, knotvector
from random import random,randint
from numpy import pi,sin,cos
from feronia.feronia import Feronia
import json
import sys
#from numba import jit

temppixels=""
jobs=0

TWOPI=2*pi
def parse_args(args):
    parser = argparse.ArgumentParser(description="WP Generator")
    parser.add_argument(
        "-o", "--out", dest="out", help="specify base output file, defaulting to wp.png"
    )
    parser.add_argument(
        "-d",
        "--dimension",
        dest="dim",
        help="specify target dimensions, i.e.: -d 800,600 (defaults to 1440,900)",
    )
    parser.add_argument(
        "--log",
        dest="loglevel",
        help="set log level:DEBUG,INFO,WARNING,ERROR,CRITICAL. The default is INFO",
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="type",
        help="set log type:lines,circle. The default is lines",
        default="LINES"
    )
    return parser.parse_args(args)


def circlespread(WIDTH,HEIGHT,RADIUS,WOBBLE,MAX_SPLINE_WIDTH,pnum):
    return [[cos(t)*RADIUS+(random()-0.5)*WOBBLE+WIDTH/2, sin(t)*RADIUS+(random()-0.5)*WOBBLE+HEIGHT/2, randint(0,MAX_SPLINE_WIDTH)]  for t in np.linspace(0, TWOPI,pnum)]


def splinei_circle(WIDTH,HEIGHT,RADIUS,MAX_SPLINE_WIDTH=120):
    curve = BSpline.Curve()
    curve.degree = 3
    curve.delta = 0.00005
    #lpoints = linespread(WIDTH,HEIGHT,MAX_SPLINE_WIDTH)
    pnum=50
    RADIUS=1000
    WOBBLE=40
    lpoints=circlespread(WIDTH,HEIGHT,RADIUS,WOBBLE,MAX_SPLINE_WIDTH,pnum)
    #print(lpoints)
    curve.degree = 3
    curve.ctrlpts = lpoints
    curve.knotvector = knotvector.generate(3, len(curve.ctrlpts))
    curve_points = curve.evalpts
    #print(len(curve_points))
    yield curve_points
    while True:
        for p in lpoints:
            p[1] += int((random() - 0.5) * (60) )
            p[0] += int((random() - 0.5) * (60) )
            p[2] += int((random() - 0.5) * (30) )
        curve.ctrlpts = lpoints
        curve_points = curve.evalpts
        yield curve_points

def splinei_basepoints_circle(WIDTH,HEIGHT,RADIUS,MAX_SPLINE_WIDTH=120):
    pnum=50
    RADIUS=1000
    WOBBLE=40
    lpoints=circlespread(WIDTH,HEIGHT,RADIUS,WOBBLE,MAX_SPLINE_WIDTH,pnum)
    #print(len(curve_points))
    yield lpoints
    while True:
        for p in lpoints:
            p[1] += int((random() - 0.5) * (60) )
            p[0] += int((random() - 0.5) * (60) )
            p[2] += int((random() - 0.5) * (30) )
        yield lpoints

def splinei_lines(WIDTH,HEIGHT,MAX_SPLINE_WIDTH=120):
    curve = BSpline.Curve()
    curve.degree = 3
    curve.delta = 0.00005
    lpoints = linespread(WIDTH,HEIGHT,MAX_SPLINE_WIDTH)
    curve.ctrlpts = lpoints
    curve.knotvector = knotvector.generate(3, len(curve.ctrlpts))
    curve_points = curve.evalpts
    yield curve_points
    while True:
        for p in lpoints:
            p[1] += ((random() - 0.5) * (25) * (sin((p[0]) * (pi / WIDTH)) ** 2))
            p[0] += ((random() - 0.5) * (5) * (sin((p[0]) * (pi / WIDTH)) ** 2))
            p[2] += ((random() - 0.5) * (10) * (sin((p[0]) * (pi / WIDTH)) ** 2))
        curve.ctrlpts = lpoints
        curve_points = curve.evalpts
        yield curve_points


def linespread(WIDTH,HEIGHT,MAX_WIDTH):
    return [[x, HEIGHT / 2, ((random() - 0.5) * (MAX_WIDTH) * (sin((x) * (pi / WIDTH))))] for x in range(0, WIDTH, 50)        ]

def merge(ch, method, properties, body):
    ldata=json.loads(body)
    global jobs
    global temppixels
    newresult=np.array(ldata['pixels'])
    WIDTH=ldata['WIDTH']
    HEIGHT=ldata['HEIGHT']
    temppixels=np.add(temppixels,newresult)
    print(newresult)
    print(newresult.max())
    jobs-=1
    
    if (jobs<=0):
        img = Image.new("RGBA", (WIDTH, HEIGHT), "white")  # create a new white image
        pixels = img.load()  # create the pixel map
        f=255/temppixels.max()
        
        temppixels=255-temppixels*f
        for x in range(WIDTH):
             for y in range(HEIGHT):
               # note: doing greyscale for now....
                pixels[x, y] = (
                    int(temppixels[x, y]),
                    int(temppixels[x, y]),
                    int(temppixels[x, y]),
                    255,
                )
      
     
        #img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        img.save("dist.png")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def gen(args=None):
    maxc=1
    global temppixels
    global jobs

    if args == None:
        args = parse_args(sys.argv[1:])
    try:
        if args.loglevel is not None:
            loglevel = getattr(logging, args.loglevel.upper(), None)
            if not isinstance(loglevel, int):
                raise ValueError("Invalid log level: %s" % args.loglevel)
            logging.basicConfig(level=loglevel)
        if args.out is not None:
            output = args.out
        else:
            output = "wp.png"
        if args.dim is not None:
            WIDTH = args.dim.split(",")[0]
            HEIGHT = args.dim.split(",")[1]
        else:
            WIDTH = 1440
            HEIGHT = 900
        if args.type is not None:
            if args.type.upper()=='LINES':
                TYPE='LINES'
            elif args.type.upper()=='CIRCLE':
                TYPE='CIRCLE'

        WIDTH*=4
        HEIGHT*=4
        temppixels=np.full((WIDTH, HEIGHT), 0.0)
        seed(23)
        img = Image.new("RGBA", (WIDTH, HEIGHT), "white")  # create a new white image
        pixels = img.load()  # create the pixel map
     
        temppixels = np.full((WIDTH, HEIGHT), 0.0)
        if TYPE=='LINES':
            sl=SpreadLines(temppixels,255)  
            curve_iterator = splinei_lines(WIDTH,HEIGHT,100)
            for _ in range(100):
                curve_points=next(curve_iterator)
                nm=sl.drawline(curve_points)
                if nm>maxc:
                    maxc=nm
        elif TYPE=='CIRCLE':
            maxc=0
            sl=SpreadLines(temppixels,255) 
            RADIUS=100
            SPREAD=100
            curve_iterator = splinei_circle(WIDTH, HEIGHT,RADIUS,SPREAD)
            for i in range(1):
                print ("loop: "+str(i))
                curve_points=next(curve_iterator)
                nm=sl.drawline(curve_points)
                if nm>maxc:
                        maxc=nm

    finally:
        print("done")  
    # except Exception as e:
    #     print("Error: {}".format(str(e)))
    # finally:
        # map the temp pixels back into the image
        # note: no list comprehension since pixels isn't a list (maybe there is a way to cast it, but I haven't found it yet)
        #since we want the image to be white, we'll inverse the generated colors
    f=1/maxc
    print("max color:" + str(maxc))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            # note: doing greyscale for now....
            pixels[x, y] = (
                int(255*(1-(f*temppixels[x, y])^2)),
                int(255*(1-(f*temppixels[x, y])^2)),
                int(255*(1-(f*temppixels[x, y])^2)),
                255,
            )
    img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
    img.save(output)

if __name__ == "__main__":
    # execute only if run as the entry point into the program
    gen()
