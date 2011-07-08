#!/usr/bin/env python3

import math
import collections

Point = collections.namedtuple('Point', ['x', 'y', 'name'])

def mkPt(x,y,n=''):
    return Point(float(x),float(y),n)

def dist(pt1, pt2):
    dx = pt2.x - pt1.x
    dy = pt2.y - pt1.y
    return math.sqrt(dx*dx+dy*dy)

class Tour(object):
    def __init__(self, fname):
        self.fname=fname
        self.pts = list()
        with open(fname) as inf:
            for nl in inf.readlines():
                self.pts.append(mkPt(*nl.strip().split(' ')))

    def __len__(self):
        return len(self.pts)

    def __getitem__(self, key):
        return self.pts[key]

    def __str__(self):
        if len(self.pts)==0:
            return ''
        if len(self.pts)==1:
            return '{}({},{}), total: {}'.format(self.pts[0].name,
                                        self.pts[0].x,
                                        self.pts[0].y,
                                                 self.cost())
        if len(self.pts)==2:
            return '{}({},{}) -({})-> {}({},{}) -({})-> {}({},{}), total: {}'.format(self.pts[0].name,
                                                            self.pts[0].x,
                                                            self.pts[0].y,
                                                            dist(self.pts[0], self.pts[1]),
                                                                                    self.pts[1].name,
                                                                                    self.pts[1].x,
                                                                                    self.pts[1].y,
                                                                                    dist(self.pts[1], self.pts[0]),
                                                            self.pts[0].name,
                                                            self.pts[0].x,
                                                            self.pts[0].y,
                                                                   self.cost())

        strVal = ''
        for i in range(0,len(self.pts)-1):
            strVal += '{}({},{}) -({})-> '.format(self.pts[i].name,
                                                    self.pts[i].x,
                                                    self.pts[i].y,
                                                    dist(self.pts[i], self.pts[i+1]))
        strVal += '{}({},{}) -({})-> {}({},{}), total: {}'.format(self.pts[-1].name,
                                               self.pts[-1].x,
                                               self.pts[-1].y,
                                               dist(self.pts[-1], self.pts[0]),
                                               self.pts[0].name,
                                               self.pts[0].x,
                                               self.pts[0].y,
                                                                    self.cost())
        return strVal

    def cost(self):
        if len(self.pts) < 2:
            return 0.0
    
        totalLen = 0
        for i in range(1, len(self.pts)):
            totalLen += dist(self.pts[i-1], self.pts[i])

        totalLen += dist(self.pts[0], self.pts[-1])
        return totalLen

