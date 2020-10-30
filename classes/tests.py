

def testItemNumbersEqual(candidate, reference):
    """Assumes Objects of Type Packer. Compares BoxItems against reference"""

    if len(candidate.boxes) == len(reference.boxes):

        for i in range(len(candidate.boxes)):

            lenBoxItemsC = len(candidate.boxes[i].items)
            lenBoxItemsR = len(reference.boxes[i].items)

            try:
                assert lenBoxItemsC == lenBoxItemsR
            except AssertionError:
                print('Number of items ( %i, %i ) in Box %i are not equal.' % 
                        (lenBoxItemsC, lenBoxItemssR, i))

