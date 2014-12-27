import operator


def get_rank_file(coord):
    return 'abcdefgh'[coord[1]] + '12345678'[coord[0]]


def get_coord_from_rank_file(rank_file_str):
    return '12345678'.index(rank_file_str[1]), 'abcdefgh'.index(rank_file_str[0])


def is_valid_sqaure(coord):
    """Check that coordinate is is valid sqaure"""
    return 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7


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