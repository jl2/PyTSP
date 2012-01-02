#!/usr/bin/env python3

import os
import sys
import os.path
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtScript

import tour

class Mapper:
    def __init__(self, xmin, xmax, ymin, ymax, width, height):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        
        self.width = width - 20
        self.height = height - 20

    def map(self, pt):
        nx = self.width * (pt[0] - self.xmin)/(self.xmax-self.xmin) +10
        ny = self.height - self.height * (pt[1] - self.ymin)/(self.ymax - self.ymin) + 10
        return (nx, ny)
    
class TspWidget(QtGui.QWidget):
    def __init__(self, tour=None, parent=None):
        super(TspWidget, self).__init__(parent)
        self.tour = tour

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHints(QtGui.QPainter.Antialiasing, True)

        if self.tour is not None:
            ul = self.tour.upperLeft()
            lr = self.tour.lowerRight()
            self.ptMap = Mapper(ul[0],lr[0],
                                lr[1], ul[1],
                                self.width(), self.height())
            self.doDrawing(qp)
        qp.end()
        
    def doDrawing(self, qp):
        blackPen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DashLine)
        redPen = QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DashLine)
        bluePen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.DashLine)
        greenPen = QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.DashLine)
        redBrush = QtGui.QBrush(QtCore.Qt.red)

        oldPt = self.ptMap.map(self.tour[0])
        
        for pt in self.tour[1:]:
            pt2 = self.ptMap.map(pt)
            
            qp.setPen(blackPen)
            qp.drawLine(oldPt[0],oldPt[1],pt2[0],pt2[1])
            qp.setPen(redPen)
            qp.drawEllipse(pt2[0]-3, pt2[1]-3, 6,6)
            oldPt = pt2

        pt2 = self.ptMap.map(self.tour[0])
        qp.setPen(blackPen)
        qp.drawLine(oldPt[0],oldPt[1],pt2[0],pt2[1])
        qp.setPen(redPen)
        qp.drawEllipse(pt2[0]-3, pt2[1]-3, 6,6)

class TspViewer(QtGui.QMainWindow):
    def __init__(self, fname = None, parent=None):
        super(TspViewer, self).__init__(parent)
        
        self.setWindowTitle("TSP Viewer")
        self.resize(800, 800)

        self.central = TspWidget()
        if fname is not None and os.path.exists(fname):
            self.central.tour = tour.Tour(fname)
            self.updateTitle(self.central.tour.cost())

        self.setCentralWidget(self.central)
        self.show()

        self.fileMenu = QtGui.QMenu('File')
        openAction = self.fileMenu.addAction('Open')
        openAction.setShortcut('Ctrl+O')

        self.connect(openAction, QtCore.SIGNAL('triggered()'), lambda: self.selectFile())

        solveAction = self.fileMenu.addAction('Solve')
        solveAction.setShortcut('Ctrl+S')
        self.connect(solveAction, QtCore.SIGNAL('triggered()'), lambda: self.solveTour())
        
        exitAction = self.fileMenu.addAction('Exit')
        self.connect(exitAction, QtCore.SIGNAL('triggered()'), lambda: self.close())
        
        self.menuBar().addMenu(self.fileMenu)

    def solveTour(self):
        if self.central.tour is not None:
            self.central.tour.solve(10000)
            self.central.update()
            self.updateTitle(self.central.tour.cost())

    def updateTitle(self, newLen):
        self.setWindowTitle('TSP Length: {newLen}'.format(newLen = newLen))
        
    def selectFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open File...', '.', '*.txt;*.*')
            
        if fname is not None:
            if os.path.exists(fname):
                self.central.tour = tour.Tour(fname)
                self.updateTitle(self.central.tour.cost())
                self.central.update()

def main(args):
    app = QtGui.QApplication([])
    fname = None
    if len(args)>0:
        fname = args[0]
    tv = TspViewer(fname)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv[1:])
