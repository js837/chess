import unittest
from position import WHITE, BLACK, DRAW
from helpers.general import new_game

class BasicMoves(unittest.TestCase):

    def test_opening_white(self):
        position=new_game()
        self.assertEqual(set(position.get_pgn_moves().keys()),
                         set(['a4','b4','c4','d4','e4','f4','g4','h4',
                              'a3','b3','c3','d3','e3','f3','g3','h3',
                              'Na3','Nc3','Nf3','Nh3']))

    def test_opening_black(self):
        position=new_game()
        self.assertEqual(set(position.get_pgn_moves(colour=BLACK).keys()),
                         set(['a6','b6','c6','d6','e6','f6','g6','h6',
                              'a5','b5','c5','d5','e5','f5','g5','h5',
                              'Na6','Nc6','Nf6','Nh6']))

    def test_king_single_move(self):
        test_board = (' K.......\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh
        position=new_game(test_board)
        pgn_moves = position.get_pgn_moves(colour=WHITE)
        self.assertEqual(set(pgn_moves.keys()), set(['Kb8','Kb7','Ka7']))

        new_position = pgn_moves['Kb7']

        test_board2 = ('........\n' #8
                       ' .K......\n' #7
                       ' ........\n' #6
                       ' ........\n' #5
                       ' ........\n' #4
                       ' ........\n' #3
                       ' ........\n' #2
                       ' ........')  #1
        # abcdefgh

        ref_position=new_game(test_board2)
        self.assertEqual(set(new_position.get_pgn_moves(WHITE).keys()),
                         set(ref_position.get_pgn_moves(WHITE).keys()))

    def test_rook(self):
        test_board = (' ........\n' #8
                      ' .....p..\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' .....R.p\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' .....p..')  #1
        # abcdefgh
        position=new_game(test_board)

        self.assertEqual(set(position.get_pgn_moves().keys()),
                         set(['Rf5','Rf6','Rg4','Rf2','Rf3','Ra4','Rb4','Rc4','Rd4','Re4',
                              'Rxf1', 'Rxf7','Rxh4']))

    def test_basic_king(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ....K...\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh

        # Need to include en-passant rights
        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['Kf4','Kf5','Kf3','Kd4','Kd5','Ke5','Ke3','Kd3']))

    def test_pawn2(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' .....n..\n' #3
                      ' .....P..\n' #2
                      ' ........')  #1
                      # abcdefgh
        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set([]))


    def test_rook_bishop(self):
        test_board = (' ........\n' #8
                      ' .....p..\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ..B..R.p\n' #4
                      ' ........\n' #3
                      ' p.......\n' #2
                      ' .....p..')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()),
                         set(['Rf5','Rf6','Rg4','Rf2','Rf3','Rd4','Re4','Bb5','Ba6','Bd5',
                              'Be6','Bb3','Bd3','Be2','Rxf1','Bxa2','Rxh4','Bxf1','Bxf7','Rxf7']))


    def test_ambiguous_rank(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' .N.N....\n' #6
                      ' ........\n' #5
                      ' ..p.....\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['Nbc8','Ndc8', 'Na8','Nd7', 'Nd5',
                                                                    'Nbxc4','Ndxc4', 'Na4', 'Nb7', 'Nb5',
                                                                    'Nf7','Nf5','Ne4','Ne8']))

    def test_ambiguous_file(self):
        test_board = (' PPPPPPPP\n' #8
                      ' PPPPPPPP\n' #7
                      ' PNPPPPPP\n' #6
                      ' PPP.PPPP\n' #5
                      ' PNPBPPPP\n' #4
                      ' PPPPPPPP\n' #3
                      ' PPPPPPPP\n' #2
                      ' PPPPPPPP')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['N6d5','N4d5']))

    def test_ambiguous_both(self):
        test_board = (' PPPPPPPP\n' #8
                      ' PPPPPPPP\n' #7
                      ' PNPPPPPP\n' #6
                      ' PPP.PPPP\n' #5
                      ' PNPBPNPP\n' #4
                      ' PPPPPPPP\n' #3
                      ' PPPPPPPP\n' #2
                      ' PPPPPPPP')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['Nb4d5','Nb6d5','Nf4d5']))


class Check(unittest.TestCase):

    def test_in_check(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' r.......\n' #3
                      ' ........\n' #2
                      ' K.......')  #1
                       # abcdefgh

        position=new_game(test_board)
        self.assertEqual(position.in_check(WHITE), True)

    def king_in_check(self):
        # Note: This would never be reached in a game.
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ...k....\n' #4
                      ' ...K....\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(position.in_check(WHITE), True)
        self.assertEqual(position.in_check(BLACK), True)

    def pawn_check(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ....p...\n' #4
                      ' ...K....\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(position.in_check(WHITE), True)

    def test_not_in_check(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ..r.....\n' #3
                      ' ........\n' #2
                      ' K.......')  #1
        # abcdefgh

        position=new_game(test_board)
        self.assertEqual(position.in_check(WHITE), False)


    def test_in_check_black_to_move(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' .r......\n' #3
                      ' ........\n' #2
                      ' .K......')  #1
        # abcdefgh

        position=new_game(test_board)
        position.active_colour = BLACK
        self.assertEqual(position.in_check(BLACK), False)


    def test_cannot_move_into_check(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' .r......\n' #3
                      ' ........\n' #2
                      ' K.......')  #1
        # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['Ka2']))


    def test_move_out_of_check(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ..b.....\n' #3
                      ' ........\n' #2
                      ' K.......')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set(['Ka2', 'Kb1']))

    def test_checkmate(self):
        test_board = (' ........\n' #8
                      ' ........\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' PPP.....\n' #2
                      ' K.q.....')  #1
                      # abcdefgh

        position=new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), set([]))

    def test_put_black_in_check(self):
        test_board = (' ...k....\n' #8
                      ' ........\n' #7
                      ' ..P.....\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' K.......')  #1
                      # abcdefgh

        position = new_game(test_board)
        self.assertEqual(set(position.get_pgn_moves().keys()), {'Kb2','Ka2','Kb1','c7+'})


class Endgame(unittest.TestCase):

    def test_white_checkmate(self):
        test_board = (' ...k...R\n' #8
                      ' .......R\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh

        position = new_game(test_board)
        self.assertEqual(position.get_moves_and_result(BLACK), ((), WHITE))

    def test_black_checkmate(self):
        test_board = (' ...K...r\n' #8
                      ' .......r\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh

        position = new_game(test_board)
        self.assertEqual(position.get_moves_and_result(WHITE), ((), BLACK))

    def test_stalemate(self):
        test_board = (' ...K....\n' #8
                      ' .......r\n' #7
                      ' ..r.r...\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' ........')  #1
                      # abcdefgh

        position = new_game(test_board)
        self.assertEqual(position.get_moves_and_result(WHITE), ((), DRAW))