import numpy as np
from abc import ABC, abstractmethod

class Packer(ABC):

    def __init__(self, items, boxes):

        self.items = items
        self.boxes = boxes

    @abstractmethod
    def pack(self):
        pass


    def validate(self):
        
        count = 0
        for c,b in enumerate(self.boxes):
            count += len(b.items)
            # print(c, len(b.items))
        
        if count == len(self.items):
            return True
        else:
            print(count)
            print(len(self.items))
            return False


class BruteForcePacker(Packer):

    def __init__(self, items, boxes):

        super().__init__(items, boxes)

    
    def pack(self):
        '''assumes boxes sorted by volume, no magic required'''

        for it in self.items:
            for b in self.boxes:
                if it <= b:
                    b.items.append(it)
                    break
            else:
                print(f'cannot fit item {it.dim}')
                continue
        return self.boxes


class RankSearchPacker(Packer):

    def __init__(self, items, boxes):

        super().__init__(items, boxes)
        
        self.initItems = self.items

    def pack(self):
        '''
        Idea goes like this: assume volume-sorted boxes, 
        sort items in one dimension, rankSearch against
        the box dimension, bigger items remain for the
        other boxes, smaller items become new input,
        repeat for next dimension. Should be quite fast
        for large N.
        '''

        for b in self.boxes:

            self.itemsLeft = []

            for i in range(3):
                T = b.dim[i]
                itSorted = sorted(self.initItems,
                        key=lambda x:x.dim[i])
                idx = self.rankSearch(itSorted, T, dim=i)
                self.itemsLeft.extend(itSorted[idx + 1:])
                self.initItems = itSorted[:idx + 1]
                
            else:
                b.items = self.initItems
                # print([it.dim[i] for it in b.items])
                self.initItems = self.itemsLeft
                
        else:
            # print(self.initItems[-1].dim)
            print(len(self.initItems), len(self.itemsLeft))


    def rankSearch(self, itemList, T, dim=0):
        '''returns the Rank of a target value in an Array'''
        L = 0
        R = len(itemList) - 1
        while L < R:
            m = (L + R) // 2
            if itemList[m].dim[dim] <= T:
                L = m + 1
            else:
                R = m
        
        '''
        Corner Case 1: List is two items long, item_0 = T,
        so R = L = 0 < len(List) -1. Return index. 
        '''
        if len(itemList) == 2:
            if itemList[0].dim[dim] <= T:
                return 0
        
        '''
        Corner Case 2: List is exhausted, L = R = len(List) - 1.
        Check if item_-1 <= T, return index.
        '''
        if L == len(itemList) - 1:
            if itemList[L].dim[dim] <= T:
                return L
            else:
                return -1
        else:
            return L - 1
