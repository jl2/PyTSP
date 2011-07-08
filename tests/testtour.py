#!/usr/bin/env python3

import os
import math

import unittest

import tour

class TestReading(unittest.TestCase):
    def setUp(self):
        with open('/tmp/empty_tour.txt', 'wt') as outf: pass

        with open('/tmp/smallfile1.txt', 'wt') as outf:
            print('0 0 bob', file=outf)
            print('0 1 tom', file=outf)
            print('1 1 jim', file=outf)
            print('1 0 sam', file=outf)

        with open('/tmp/smallfile2.txt', 'wt') as outf:
            print('0 0', file=outf)
            print('1 1', file=outf)
            print('1 0', file=outf)

        with open('/tmp/smallfile3.txt', 'wt') as outf:
            print('0 0', file=outf)
            print('1 0', file=outf)

        with open('/tmp/smallfile4.txt', 'wt') as outf:
            print('0 0 wtf', file=outf)

    def tearDown(self):
        os.remove('/tmp/empty_tour.txt')
        os.remove('/tmp/smallfile1.txt')
        os.remove('/tmp/smallfile2.txt')
        os.remove('/tmp/smallfile3.txt')
        os.remove('/tmp/smallfile4.txt')
        
    def test_read(self):
        myTour = tour.Tour('/tmp/smallfile1.txt')
        self.assertEqual(4, len(myTour))
        self.assertEqual(0.0, myTour[1].x)
        self.assertEqual(1.0, myTour[1].y)
    

    def test_dist(self):
        self.assertEqual(1.0, tour.dist(tour.mkPt(0,0),
                                        tour.mkPt(1,0)))
        self.assertEqual(1.0, tour.dist(tour.mkPt(0,0),
                                        tour.mkPt(0,1)))

        self.assertEqual(0.0, tour.dist(tour.mkPt(0,0),
                                        tour.mkPt(0,0)))

        self.assertEqual(math.sqrt(2), tour.dist(tour.mkPt(0,0),
                                                 tour.mkPt(1,1)))

    def test_tour_len1(self):
        t1 = tour.Tour('/tmp/empty_tour.txt')
        self.assertEqual(0.0, t1.cost())

        t2 = tour.Tour('/tmp/smallfile1.txt')
        self.assertEqual(4, t2.cost())

        t3 = tour.Tour('/tmp/smallfile2.txt')
        self.assertEqual(1+1+math.sqrt(2), t3.cost())

    def test_tour_str(self):

        t1 = tour.Tour('/tmp/empty_tour.txt')
        self.assertEqual('', str(t1))

        t2 = tour.Tour('/tmp/smallfile1.txt')
        self.assertEqual('bob(0.0,0.0) -(1.0)-> tom(0.0,1.0) -(1.0)-> jim(1.0,1.0) -(1.0)-> sam(1.0,0.0) -(1.0)-> bob(0.0,0.0), total: 4.0', str(t2))
        
        t3 = tour.Tour('/tmp/smallfile2.txt')
        self.assertEqual('(0.0,0.0) -(1.4142135623730951)-> (1.0,1.0) -(1.0)-> (1.0,0.0) -(1.0)-> (0.0,0.0), total: 3.414213562373095', str(t3))

        t4 = tour.Tour('/tmp/smallfile3.txt')
        self.assertEqual('(0.0,0.0) -(1.0)-> (1.0,0.0) -(1.0)-> (0.0,0.0), total: 2.0', str(t4))

        t5 = tour.Tour('/tmp/smallfile4.txt')
        self.assertEqual('wtf(0.0,0.0), total: 0.0', str(t5))

if __name__=='__main__':
    unittest.main()
