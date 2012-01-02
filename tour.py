#!/usr/bin/env python3

import math
import random
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
        ul = (9999999,-9999999)
        lr = (-9999999,9999999)
        
        with open(fname) as inf:
            for nl in inf.readlines():
                np = mkPt(*nl.strip().split(' '))
                self.pts.append(np)
                if np[0] < ul[0]:
                    ul = (np[0],ul[1])
                if np[1] > ul[1]:
                    ul = (ul[0], np[1])

                if np[0]>lr[0]:
                    lr = (np[0], lr[1])
                if np[1] < lr[1]:
                    lr = (lr[0], np[1])
        self.ul = ul
        self.lr = lr

    def __len__(self):
        return len(self.pts)

    def __getitem__(self, key):
        return self.pts[key]
    
    def __str__(self):
        if len(self.pts)==0:
            return ''

        if len(self.pts)==1:
            return ('{}({},{}), total: {}'
                    ).format(self.pts[0].name, self.pts[0].x, self.pts[0].y,
                             self.cost())

        # Is this even a valid case?
        if len(self.pts)==2:
            return ('{}({},{}) -({})-> {}({},{}) -({})-> {}({},{}), total: {}'
                    ) .format(self.pts[0].name, self.pts[0].x, self.pts[0].y,
                              dist(self.pts[0], self.pts[1]),
                              self.pts[1].name, self.pts[1].x, self.pts[1].y,
                              dist(self.pts[1], self.pts[0]),
                              self.pts[0].name, self.pts[0].x, self.pts[0].y,
                              self.cost())

        strVal = ''
        for i in range(0,len(self.pts)-1):
            strVal += ('{}({},{}) -({})-> '
                       ).format(self.pts[i].name, self.pts[i].x, self.pts[i].y,
                                dist(self.pts[i], self.pts[i+1]))

        strVal += ('{}({},{}) -({})-> {}({},{}), total: {}'
                   ).format(self.pts[-1].name, self.pts[-1].x, self.pts[-1].y,
                            dist(self.pts[-1], self.pts[0]),
                            self.pts[0].name, self.pts[0].x, self.pts[0].y,
                            self.cost())
        return strVal

    def upperLeft(self):
        return self.ul

    def lowerRight(self):
        return self.lr
    
    def save(self, fname):
        with open(fname, 'wt') as outf:
            for pt in self.pts:
                print('{} {}'.format(*pt), file=outf)

    
    def cost(self):
        if len(self.pts) < 2:
            return 0.0
    
        totalLen = 0
        for i in range(1, len(self.pts)):
            totalLen += dist(self.pts[i-1], self.pts[i])

        totalLen += dist(self.pts[0], self.pts[-1])
        return totalLen

    def solve(self, iters=10):
        for i in range(0,iters):
            a = random.randint(1, len(self.pts)-2)
            b = a
            while a==b:
                b = random.randint(a, len(self.pts)-1)
            
            oc = self.cost()
            for j in range(0,b-a):
                tmp = self.pts[j + a]
                self.pts[j+a] = self.pts[b-j]
                self.pts[b-j] = tmp
            nc = self.cost()
            if nc>oc:
                for j in range(0,b-a):
                    tmp = self.pts[j + a]
                    self.pts[j+a] = self.pts[b-j]
                    self.pts[b-j] = tmp


