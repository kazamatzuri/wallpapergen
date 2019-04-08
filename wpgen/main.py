import os, sys
import argparse
from random import seed
import logging
from PIL import Image
import numpy as np
from spreadlines.spreadlines import SpreadLines
from geomdl import BSpline, knotvector
from random import random
from numpy import pi,sin
from numba import jit

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
    return parser.parse_args(args)


def splinei(WIDTH,HEIGHT):
    curve = BSpline.Curve()
    curve.degree = 3
    curve.delta = 0.00005
    lpoints = linespread(WIDTH,HEIGHT)
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


def linespread(WIDTH,HEIGHT):
    return [[x, HEIGHT / 2, ((random() - 0.5) * (120) * (sin((x) * (pi / WIDTH))))] for x in range(0, WIDTH, 50)        ]

def gen(args=None):
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

        WIDTH*=4
        HEIGHT*=4
        img = Image.new("RGBA", (WIDTH, HEIGHT), "white")  # create a new white image
        pixels = img.load()  # create the pixel map
        seed()
        # we use temppixels, because to get nice results we need to do the color calc in float
        # not in ints....
        #we'll start out with all black
        temppixels = np.full((WIDTH, HEIGHT), 0.0)

        sl=SpreadLines(temppixels,5)
        
        curve_iterator = splinei(WIDTH,HEIGHT)

        for _ in range(100):
            curve_points=next(curve_iterator)
            sl.drawline(curve_points)
        
        # map the temp pixels back into the image
        # note: no list comprehension since pixels isn't a list (maybe there is a way to cast it, but I haven't found it yet)
        #since we want the image to be white, we'll inverse the generated colors
        for x in range(WIDTH):
            for y in range(HEIGHT):
                # note: doing greyscale for now....
                pixels[x, y] = (
                    255-int(temppixels[x, y]),
                    255-int(temppixels[x, y]),
                    255-int(temppixels[x, y]),
                    255,
                )
        img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        img.save(output)
    except OSError as e:
        print("Error: {}".format(str(e)))


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    gen()
