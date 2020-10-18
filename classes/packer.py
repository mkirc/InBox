import numpy as np
from abc import ABC, abstractmethod
from bisect import bisect
from collections import deque

class Packer(ABC):
    """idx = bisect(keys, T)"""

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


class LinearSearchPacker(Packer):
    """Iterates through items, compares each dimension
    with boxes'."""

    def __init__(self, items, boxes):

        super().__init__(items, boxes)

    
    def pack(self):

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
        """Sort items in one dimension, rankSearch against the box 
        dimension, bigger items remain for the other boxes, smaller
        items become new input, repeat for next dimension."""

    def __init__(self, items, boxes):

        super().__init__(items, boxes)
        
        self._items = self.items

    def pack(self):

        for b in self.boxes:

            self.itemsLeft = []

            for i in range(3):
                T = b.dim[i]
                itSorted = sorted(self._items,
                        key=lambda x:x.dim[i])
                idx = self.rankSearch(itSorted, T, dim=i)
                self.itemsLeft.extend(itSorted[idx + 1:])
                self._items = itSorted[:idx + 1]
                
            else:
                b.items = self._items
                # print([it.dim[i] for it in b.items])
                self._items = self.itemsLeft
                
        # else:
        #     # print(self._items[-1].dim)
        print(len(self.items), len(self._items), len(self.itemsLeft))



    def rankSearch(self, itemList, T, dim=0):
        """returns the Rank of a target value in an Array"""
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

class BisectPacker(Packer):
    """Remember the RSP from line 52?
    this is basically the same thing,
    only with a python implementation
    of rank search"""

    def __init__(self, items, boxes):

        super().__init__(items, boxes)

        self._items = self.items

    def pack(self):
        
        for b in self.boxes:

            self.itemsLeft = []

            for i in range(3):
                
                T = b.dim[i]

                itSorted = sorted(self._items,
                        key=lambda x:x.dim[i])

                keys = [it.dim[i] for it in itSorted] # compute the keylist
                idx = bisect(keys, T) # perform the search
                self.itemsLeft.extend(itSorted[idx:])
                self._items = itSorted[:idx]
            else:
                b.items = self._items
                # print([it.dim[i] for it in b.items])
                self._items = self.itemsLeft
                
        else:
            # print(self._items[-1].dim)
            print(len(self.items), len(self._items), len(self.itemsLeft))


class BisectAndDiffPacker(Packer):
    """Compute one sorted list per dimension d[i], rank search them,
    store lower and higher indices in seperate lists, find the
    intersection of the d lower ones. Prepend the symmetric
    difference (list equivalent, since we want to preserve order)
    to the eliminated higher indices, continue.""" 

    
    def __init__(self, items, boxes):

        super().__init__(items, boxes)

        self.getKeys()

    def getKeys(self):
        """Compute one sorted list per dimension"""

        self._items = []

        for i in range(3):

            x = sorted(self.items,
                    key=lambda x:x.dim[i])
            self._items.append(x)

    def pack(self):
        
        for b in self.boxes:
            
            candidates = []
            itemsLeft = []
            
            for i in range(3):
                
                T = b.dim[i]
                itList = self._items[i]
                idx = self.rankSearch(itList, T, dim=i)
                candidates.append(self._items[i][:idx+1])
                itemsLeft.append(deque(self._items[i][idx+1:]))
            else:
                intersection = set(candidates[0]) \
                        & set(candidates[1]) \
                        & set(candidates[2])
                
                b.items = intersection
                
                for i in range(3):

                    fools = [x for x in candidates[i] if x not in intersection]
                    fools.reverse() 
                    itemsLeft[i].extendleft(fools)
                    
                    self._items[i] = list(itemsLeft[i])


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
