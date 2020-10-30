import numpy as np
from classes.control import PackingController, Timer
from classes.test import Tester

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
    
    tester = Tester()
    t = Timer()

    pc.initRSP()
    pc.initLSP()
    pc.initBP()
    pc.initBDP()
    
    t.start()
    pc.lsp.pack()
    t.stop()
    print(pc.lsp.validate())
    
    # t.start()
    # pc.rsp.pack()
    # t.stop()   
    # print(pc.rsp.validate())

    # t.start()
    # pc.bp.pack()
    # t.stop()    
    # print(pc.bp.validate())
    

    t.start()
    pc.bdp.pack()
    t.stop()    
    print(pc.bdp.validate())
    
    tester.testItemNumbersEqual(pc.lsp, pc.bdp)



if __name__ == '__main__':
    run()
