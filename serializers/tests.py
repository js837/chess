__author__ = 'Jake'

import unittest
from serializers import PositionSerializer
from helpers.general import new_game


class Serializers(unittest.TestCase):

    def test_opening_from_FEN(self):
        position=new_game()
        new_position = PositionSerializer.from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.assertEqual(str(new_position), str(position))

    def test_opening_to_FEN(self):
        position=new_game()
        fen_opening = PositionSerializer.to_fen(position)
        fen_opening_constant = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.assertEqual(fen_opening, fen_opening_constant)

    def test_opening_first_move_to_FEN(self):
        position=new_game()

        position = position.get_pgn_moves()['e4']
        self.assertEqual(PositionSerializer.to_fen(position), 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1')

        position = position.get_pgn_moves()['c5']
        self.assertEqual(PositionSerializer.to_fen(position), 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2')

        position = position.get_pgn_moves()['Nf3']
        self.assertEqual(PositionSerializer.to_fen(position), 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
