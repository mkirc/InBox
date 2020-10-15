import numpy as np
from classes.point import ItemBoxFactory
from classes.packer import BruteForcePacker, RankSearchPacker

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

    def initBFP(self):
        
        self.bfp = BruteForcePacker(self.items, self.boxes)

    def initRSP(self):

        self.rsp = RankSearchPacker(self.items, self.boxes)
