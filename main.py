#!/usr/bin/env python3

import sys
import common
import os.path
import argparse

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument( '--infile', type=os.path.abspath, required=True)
    conf, unknown = parser.parse_known_args(args)

    tour = common.readTour(conf.infile)
    print('Tour has length:', common.tourLen(tour))
    
if __name__=='__main__':
    main(sys.argv[1:])
