#!/usr/bin/env python3

import sys
import shutil
import os.path
import argparse

import tour
import svgimg

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument( '--infile', type=os.path.abspath, required=True)
    conf, unknown = parser.parse_known_args(args)

    tr = tour.Tour(conf.infile)
    print('Tour has length:', tr.cost())
    tr.solve(500000)
    print('New tour has length:',tr.cost())
    toImg = svgimg.Svg()
    for i in range(len(tr.pts)-1):
        toImg.add_line([tr[i], tr[i+1]])
    toImg.add_line([tr[-1], tr[0]])
    # toImg.add_pts(tr.pts)
    with open('testit.svg', 'wt') as outf:
        print(toImg, file=outf)
    shutil.copy(conf.infile, conf.infile+'.bak')
    tr.save(conf.infile)

    
if __name__=='__main__':
    main(sys.argv[1:])
