import operator




class Coord(tuple):
    """
    Basic coordinate class, length 2 to allow adding of 2-tuples
    """
    @staticmethod
    def __new__(cls, x, y):
        # Creation via args
        return tuple.__new__(cls, (x,y))

    def __add__(self, other):
        return Coord(self[0]+other[0], self[1]+other[1])

    def __sub__(self, other):
        return Coord(self[0]-other[0], self[1]-other[1])



N, E, S, W, NE, SE, SW, NW, N2, S2 = Coord(1,0), Coord(0,1), Coord(-1,0), Coord(0,-1), Coord(1,1), Coord(-1,1),\
                                     Coord(-1, -1), Coord(1, -1), Coord(2, 0), Coord(-2,0)