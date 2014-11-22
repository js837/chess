import unittest
from helpers.general import new_game
from position import WHITE, BLACK

class Pawns(unittest.TestCase):

    def test_normal_pawn_capture(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' .P..p.p.\n' #5
                      ' .....P..\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' ........')  #1
        # abcdefgh


        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['xe5','xg5','b6', 'f5']))

    def test_pawn_en_passant(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ..p.....\n' #4
                      ' ........\n' #3
                      ' .P......\n' #2
                      ' ........')  #1
        # abcdefgh

        position=new_game(test_board)

        move_dict = position.get_pgn_moves() #b4, b3
        double_move_position = move_dict['b4']

        self.assertEqual(double_move_position.en_passant, (2, 1))
        move_dict = double_move_position.get_pgn_moves() #c3, b3
        self.assertEqual(set(move_dict.keys()), set(['c3', 'cxb3e.p.']))

        en_passant_capture_position = move_dict['cxb3e.p.']
        self.assertEqual(en_passant_capture_position.en_passant, None)
        self.assertEqual(set(en_passant_capture_position.get_pgn_moves().keys()), set([]))


    def test_pawn_check(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' .p......\n' #2
                      ' K.......')  #1
                      # abcdefgh
        position=new_game(test_board)
        self.assertEqual(position.in_check(WHITE), True)

    def test_en_passent_only_for_pawns(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ..b.....\n' #4
                      ' ........\n' #3
                      ' .P......\n' #2
                      ' ........')  #1
                      # abcdefgh

        position=new_game(test_board)

        move_dict = position.get_pgn_moves() #b4, b3
        double_move_position = move_dict['b4']

        self.assertEqual(double_move_position.en_passant, (2, 1))

        move_dict = double_move_position.get_pgn_moves()
        self.assertEqual(set(move_dict.keys()), set(['Ba6','Ba2','Bd5','Bg8','Bf1','Bf7',
                                                     'Bd3','Be2','Bb5','Be6','Bb3']))

        en_passant_capture_position = move_dict['Ba6']
        self.assertEqual(en_passant_capture_position.en_passant, None)
        self.assertEqual(set(en_passant_capture_position.get_pgn_moves().keys()), set(['b5']))

    def test_pawn_promotion(self):
        test_board = (' ........\n' #8
                      ' ....P...\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh
        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves(WHITE).keys()), {'e8Q','e8B','e8R','e8N'})







class Castling(unittest.TestCase):

    def test_castling_white(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' p...p..p\n' #4
                      ' P...P..P\n' #3
                      ' P...P..P\n' #2
                      ' R...K..R')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['Rg1','Rf1','Rd1','Kf1','Rc1','Kf2','Kd2',
                                                                    'Kd1','Rb1', 'O-O', 'O-O-O']))


    def test_castling_black(self):
        test_board = (' r...k..r\n' #8
                      ' pppppppp\n' #7
                      ' pppppppp\n' #6
                      ' pppppppp\n' #5
                      ' pppppppp\n' #4
                      ' pppppppp\n' #3
                      ' pppppppp\n' #2
                      ' pppppppp')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves(BLACK).keys()), {'Rb8', 'Rc8','Rd8','Rg8','Rf8',
                                                                     'Kd8','Kf8','O-O','O-O-O'})


    def test_castling_black_king_side(self):
        test_board = (' rpppk..r\n' #8
                      ' pppppppp\n' #7
                      ' pppppppp\n' #6
                      ' pppppppp\n' #5
                      ' pppppppp\n' #4
                      ' pppppppp\n' #3
                      ' pppppppp\n' #2
                      ' pppppppp')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves(BLACK).keys()), set(['Rg8','Rf8','Kf8','O-O']))

    def test_castling_through_check(self):
        test_board = (' PPPPPPPP\n' #8
                      ' PPPPPPPP\n' #7
                      ' PPPPPPPP\n' #6
                      ' PPPPPPPP\n' #5
                      ' PPPPPPPP\n' #4
                      ' PPPPPPPP\n' #3
                      ' PPpPPPPP\n' #2
                      ' R...K..R')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['Rg1','Rf1','Rd1','Kf1','Rc1', 'Rb1', 'O-O']))

    def test_castling_after_king_moved(self):
        test_board = (' PPPPPPPP\n' #8
                      ' PPPPPPPP\n' #7
                      ' PPPPPPPP\n' #6
                      ' PPPPPPPP\n' #5
                      ' PPPPPPPP\n' #4
                      ' PPPPPPPP\n' #3
                      ' PPPPPPPP\n' #2
                      ' R...K..R')  #1
                      # abcdefgh

        position=new_game(test_board)

        king_move1 = position.get_pgn_moves(WHITE)['Kd1']
        king_move2 = king_move1.get_pgn_moves(WHITE)['Ke1']
        self.assertEqual(set(king_move2.get_pgn_moves(WHITE).keys()), set(['Kd1','Kf1','Rg1','Rf1','Rd1','Rc1', 'Rb1']))


    def test_castling_after_queen_rook_moved_white(self):
        test_board = (' PPPPPPPP\n' #8
                      ' PPPPPPPP\n' #7
                      ' PPPPPPPP\n' #6
                      ' PPPPPPPP\n' #5
                      ' PPPPPPPP\n' #4
                      ' PPPPPPPP\n' #3
                      ' PPPPPPPP\n' #2
                      ' R...K..R')  #1
                      # abcdefgh

        position=new_game(test_board)
        rook_move1 = position.get_pgn_moves(WHITE)['Rb1']
        rook_move2 = rook_move1.get_pgn_moves(WHITE)['Ra1']
        self.assertEqual(set(rook_move2.get_pgn_moves(WHITE).keys()), set(['Kd1','Kf1','Rg1','Rf1','Rd1','Rc1', 'Rb1','O-O']))


    def test_castling_after_king_rook_moved_white(self):
        test_board = (' PPPPPPPP\n' #8
                      ' PPPPPPPP\n' #7
                      ' PPPPPPPP\n' #6
                      ' PPPPPPPP\n' #5
                      ' PPPPPPPP\n' #4
                      ' PPPPPPPP\n' #3
                      ' PPPPPPPP\n' #2
                      ' R...K..R')  #1
                      # abcdefgh

        position=new_game(test_board)
        rook_move1 = position.get_pgn_moves(WHITE)['Rg1']
        rook_move2 = rook_move1.get_pgn_moves(WHITE)['Rh1']
        self.assertEqual(set(rook_move2.get_pgn_moves(WHITE).keys()), set(['Kd1','Kf1','Rg1','Rf1','Rd1','Rc1', 'Rb1','O-O-O']))

    def test_castling_after_king_moved_black(self):
        test_board = (' r...k..r\n' #8
                      ' pppppppp\n' #7
                      ' pppppppp\n' #6
                      ' pppppppp\n' #5
                      ' pppppppp\n' #4
                      ' pppppppp\n' #3
                      ' pppppppp\n' #2
                      ' pppppppp')  #1
                      # abcdefgh

        position=new_game(test_board)
        rook_move1 = position.get_pgn_moves(BLACK)['Rg8']
        rook_move2 = rook_move1.get_pgn_moves(BLACK)['Rh8']
        self.assertEqual(set(rook_move2.get_pgn_moves(BLACK).keys()), set(['Kd8','Kf8','Rg8','Rf8','Rd8','Rc8', 'Rb8','O-O-O']))


    def test_castling_after_queen_rook_moved_black(self):
        test_board = (' r...k..r\n' #8
                      ' pppppppp\n' #7
                      ' pppppppp\n' #6
                      ' pppppppp\n' #5
                      ' pppppppp\n' #4
                      ' pppppppp\n' #3
                      ' pppppppp\n' #2
                      ' pppppppp')  #1
                      # abcdefgh

        position=new_game(test_board)
        rook_move1 = position.get_pgn_moves(BLACK)['Rb8']
        rook_move2 = rook_move1.get_pgn_moves(BLACK)['Ra8']
        self.assertEqual(set(rook_move2.get_pgn_moves(BLACK).keys()), set(['Kd8','Kf8','Rg8','Rf8','Rd8','Rc8', 'Rb8','O-O']))


    def test_castling_after_king_rook_moved_black(self):
        test_board = (' r...k..r\n' #8
                      ' pppppppp\n' #7
                      ' pppppppp\n' #6
                      ' pppppppp\n' #5
                      ' pppppppp\n' #4
                      ' pppppppp\n' #3
                      ' pppppppp\n' #2
                      ' pppppppp')  #1
                      # abcdefgh

        position=new_game(test_board)
        rook_move1 = position.get_pgn_moves(BLACK)['Rg8']
        rook_move2 = rook_move1.get_pgn_moves(BLACK)['Rh8']
        self.assertEqual(set(rook_move2.get_pgn_moves(BLACK).keys()), set(['Kd8','Kf8','Rg8','Rf8','Rd8','Rc8', 'Rb8','O-O-O']))
