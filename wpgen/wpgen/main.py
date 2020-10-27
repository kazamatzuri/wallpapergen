import argparse
import logging
import sys

from core import Core


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
            WIDTH = None
            HEIGHT = None
        core = Core(width=WIDTH, height=HEIGHT)

    finally:
        print("done")

    print("end")
