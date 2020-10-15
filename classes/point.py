import numpy as np

class Point():

    def __init__(self, xyzList):

        self.dim = np.array(xyzList)
    
    def __lt__(self, other):

        for i in range(3):
            if self.dim[i] < other.dim[i]:
                continue
            else:
                break
        else:
            return True
        
        return False

    def __le__(self, other):

        for i in range(3):
            if self.dim[i] <= other.dim[i]:
                continue
            else:
                break
        else:
            return True
        
        return False



class Item(Point):

    def __init__(self, xyzList):

        coords = sorted(xyzList, reverse=True)

        super().__init__(coords)

class Box(Point):

    def __init__(self, xyzList):

        coords = sorted(xyzList, reverse=True)

        super().__init__(coords)
        
        self.items = []
        

class PointFactory():

    def __init__(self):

        pass

    def makeItem(self, cList):       
        
        return Item(cList)

    def makeBox(self, cList):
        
        return Box(cList)

class ItemBoxFactory():

    def __init__(self):

        self.pf = PointFactory()
        self.itemBoxes = []

    def loadCSV(self, path, boxOnly=False):
        print('loading points from %s' % (path))
        
        with open(path) as openFile:
            for line in openFile:
                self.parse(line, boxOnly)

    def parse(self, line, boxOnly):

        line = [i.strip() for i in line.split(',')]
        
        boxDims = [int(line[1]), int(line[2]), int(line[3])]
        
        if not boxOnly:
            itemDims = [int(line[4]), int(line[5]), int(line[6])]
            item = self.pf.makeItem(itemDims)
        else:
            item = []
        box = self.pf.makeBox(boxDims)

        return self.itemBoxes.append([item, box])

    def getItemBoxes(self, numPoints=None):

        if numPoints is not None:
            return self.itemBoxes[:numPoints]
        else:
            return self.itemBoxes
    
    def getSampleWithReplacement(self, n=1111, seed=11):
        
        np.random.seed(seed)
        idxs = [i for i in range(len(self.itemBoxes))]
        idxList = np.random.choice(idxs, size=n, replace=True)
        smp = []
        for i in idxList:
            smp.append(self.itemBoxes[i])
        return smp

    def reset(self):

        self.itemBoxes = []
