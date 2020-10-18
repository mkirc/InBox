import numpy as np
from time import perf_counter
from classes.point import ItemBoxFactory
from classes.packer import LinearSearchPacker
from classes.packer import RankSearchPacker
from classes.packer import BisectPacker
from classes.packer import BisectAndDiffPacker

class PackingController():

    def __init__(self):

        self.ibf = ItemBoxFactory()
        self.boxes = []
        self.items = []

    def loadItems(self, inPath):

        self.ibf.loadCSV(inPath)
        self.items = [ibs[0] for ibs in self.ibf.itemBoxes]
        self.ibf.reset()

    def loadBoxes(self, inPath):

        self.ibf.loadCSV(inPath, boxOnly=True)
        self.boxes = [ibs[1] for ibs in self.ibf.itemBoxes]
        self.ibf.reset()

    def sortBoxesByVolume(self):
        
        self.boxes = sorted(self.boxes, 
                key=lambda x:(x.dim[0] * x.dim[1] * x.dim[2]))

    def initLSP(self):
        
        self.lsp = LinearSearchPacker(self.items, self.boxes)

    def initRSP(self):

        self.rsp = RankSearchPacker(self.items, self.boxes)

    def initBP(self):
        self.bp = BisectPacker(self.items, self.boxes)

    def initBDP(self):

        self.bdp = BisectAndDiffPacker(self.items, self.boxes)


class TimerError(Exception):
    """custom Timer exception"""

class Timer():

    def __init__(self):

        self._startTime = None

    def start(self):

        if self._startTime is not None:
            raise TimerError(f'Timer is running, use stop() to stop it.')
        else:
            self._startTime = perf_counter()

    def stop(self):

        if self._startTime is None:
            raise TimerError(f'Timer is not running, use start() to start it.')
        else:

            elapsedTime = perf_counter() - self._startTime
            
            print('Elapsed Time: %0.4f seconds.' % (elapsedTime))

            self._startTime = None

            return elapsedTime


