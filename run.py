import numpy as np
from classes.control import PackingController

def prettyPrint(boxList):

    for c,b in enumerate(boxList):
        vol = b.dim[0] * b.dim[1] * b.dim[2]
        print('%i   %i' % (c, vol))

def run():
    
    itemsPath = 'assets/data_new_biggest_02.csv'
    boxesPath = 'assets/boxes_orig.csv'
    samplePath = 'assets/sample_n-25000.csv'
    minPath = 'assets/sample_min.csv'
    pc = PackingController()
    pc.loadItems(itemsPath)
    print('%i items loaded.' % len(pc.items))
    pc.loadBoxes(boxesPath)
    print('%i boxes loaded.' % len(pc.boxes))
    pc.sortBoxesByVolume()
    
    pc.initRSP()
    pc.initBFP()
    pc.bfp.pack()
    print(pc.bfp.validate())
    pc.rsp.pack()
    print(pc.rsp.validate())

    

run()
