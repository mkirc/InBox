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

            # iterate over dimensions
            for i in range(3):
                T = b.dim[i]
                # sort in current dimension
                itSorted = sorted(self._items,
                        key=lambda x:x.dim[i]) 
                # get index of highest value still fitting
                idx = rankSearch(itSorted, T, dim=i)
                # put larger items into itemLeft 
                self.itemsLeft.extend(itSorted[idx + 1:])
                '''put smaller items into _items, so we can take them
                into the next iteration step'''
                self._items = itSorted[:idx + 1]
                
            else:
                '''now we iterated over all dimensions. assign _items to
                the corresponding box, set _items to itemsLeft, so we have them
                ready for the next box'''
                b.items = self._items
                # print([it.dim[i] for it in b.items])
                self._items = self.itemsLeft
                
        # else:
        #     # print(self._items[-1].dim)
        print(len(self.items), len(self._items), len(self.itemsLeft))



class BisectPacker(Packer):
    """Remember the RSP from above?
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
        return

    def pack(self):
        
        for b in self.boxes:
            
            candidates = []
            itemsLeft = []
            
            for i in range(3):
                
                # here we get the target for the ranksearch
                T = b.dim[i]
                # get the list to perform the ranksearch on
                itList = self._items[i]
                idx = rankSearch(itList, T, dim=i)
                # put boxes with smaller dimension into candidates
                candidates.append(self._items[i][:idx+1])
                '''put lager ones into itemsLeft. note, that we use
                a deque, so we can extend the list to the left later'''
                itemsLeft.append(deque(self._items[i][idx+1:]))
            else:
                '''after we built our candidates, compute the intersection of all three
                lists. Note that set() is performed on the Item(Point)-objects.'''

                intersection = set(candidates[0]) \
                        & set(candidates[1]) \
                        & set(candidates[2])
                
                # assign the items in the intersection to the target box
                b.items = intersection
                
                '''of course not all items made it into our final intersection.
                i call them fools, because locally they seemed like a good choice,
                but at least on dimension didnt check out'''
                
                for i in range(3):
                    
                    '''sort fools by their dimensions. note, that we use
                    condidates for building the list, since we want to retain
                    their order, which set() destroyed in intersection'''
                    fools = [x for x in candidates[i] if x not in intersection]
                    '''we have to reverse fools, because extendleft() reads the list
                    starting from the highest index in reverse'''
                    fools.reverse() 
                    itemsLeft[i].extendleft(fools)
                    
                    # last but not least we prepare _items for the next round
                    self._items[i] = list(itemsLeft[i])


def rankSearch(itemList, T, dim=0):
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
