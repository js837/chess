import unittest
from .coord import Coord


class TestCoord(unittest.TestCase):

    def test_coord(self):
        self.assertEqual(Coord(1,1)+Coord(2,2), Coord(3,3))