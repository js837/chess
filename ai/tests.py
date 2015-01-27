import cProfile
import unittest

from helpers.general import new_game
from algorithms import MinimaxLookahead
from basic import ShannonAI
from serializers import PositionSerializer
import time


class Evaluation(unittest.TestCase):


    def test_new_eval_method(self):
        position = new_game()
        t0 = time.time()
        move_tree = MinimaxLookahead.breadth_search(position, depth=6)
        t1 = time.time()
        print t1-t0
        print len(move_tree)

        #for position, depth in move_tree:
        #    ShannonAI.evaluate(position)
        #t2 = time.time()
        #print t2-t1





    def test_eval(self):
        position = new_game()
        self.assertIsInstance(ShannonAI.evaluate(position), (float, int))


    def test_position_metric(self):
        position = new_game()
        for i,move in enumerate(position.get_moves()):
            print i, ShannonAI.evaluate(move, colour=position.active_colour)
            print move



    def test_obvious_move(self):
        test_board = (' .K......\n' #8
                      ' ...Q..q.\n' #7
                      ' ........\n' #6
                      ' ........\n' #5
                      ' ........\n' #4
                      ' ........\n' #3
                      ' ........\n' #2
                      ' k.......')  #1
                      # abcdefgh
        position = new_game(test_board)
        best_fen = '1K6/6Q1/8/8/8/8/8/k7 b KQkq - 0 1'
        best_move = ShannonAI.get_best_move(position, depth=1)
        self.assertEqual(PositionSerializer.to_fen(best_move), best_fen)


    #def test_minimax(self):
    #    test_board = (' QP...K..\n' #8
    #                  ' .p......\n' #7
    #                  ' p.......\n' #6
    #                  ' ........\n' #5
    #                  ' ........\n' #4
    #                  ' ........\n' #3
    #                  ' ........\n' #2
    #                  ' ......k.')  #1
    #                  # abcdefgh
    #
    #    position = new_game(test_board)
    #    tree={}
    #    moves = [(position,0)]
    #    max_depth = 4
    #    while moves:
    #        move, depth = moves.pop()
    #        new_moves = move.get_moves()
    #        for new_move in new_moves:
    #            moves.append((move, depth+1))
    #            tree[new_move, depth+1] = (move, depth)
    #        moves = filter(lambda x: x[1] < max_depth, moves) # Only include moves than are less than n deep
    #
    #
    #    leaves = filter(lambda x:x[1]==max_depth,tree.keys())
    #
    #
    #    import pdb; parity = 1-2*(max_depth % 2)
    #    best_move = max(leaves, key=lambda x: parity*ShannonAI.evaluate(x[0]))
    #
    #    pdb.set_trace()
    #
    #
    #    self.assertIsInstance(ShannonAI.evaluate(position), (float, int))

    def test_problem_easy(self):
        # White to mate in 1 move
        position = PositionSerializer.from_fen('2n5/8/6R1/1k1KQb2/2N1N3/8/R2B4/r1n2B2 w - - 0 1')
        mate=position.get_pgn_moves()['Kd4+']
        move = ShannonAI.get_best_move(position, depth=2)
        self.assertEqual(mate, move)

    def test_problem_easy2(self):
        # White to mate in 1 move
        position = PositionSerializer.from_fen('2n5/8/6R1/1k1KQb2/2N1N3/8/R2B4/r1n2B2 w - - 0 1')
        mate=position.get_pgn_moves()['Kd4+']
        move = ShannonAI.get_best_move(position, depth=2)
        self.assertEqual(mate, move)

    def test_problem_easy3(self):
        # White to mate in 2 moves
        position = PositionSerializer.from_fen('rR6/2n5/k1p3r1/5pp1/PR5p/7P/3B1PP1/5K2 w - - 0 1')
        mate=position.get_pgn_moves()['R4b6+']
        move = ShannonAI.get_best_move(position, depth=4)
        self.assertEqual(mate, move)


    def test_move_tree_speed(self):
        position = PositionSerializer.from_fen('rR6/2n5/k1p3r1/5pp1/PR5p/7P/3B1PP1/5K2 w - - 0 1')

        start = time.time()

        profile = cProfile.Profile()
        profile.enable()
        move_tree = MinimaxLookahead.breadth_search(position,depth=3)
        profile.disable()
        profile.print_stats(sort='time')


        end = time.time()

        print '{} moves'.format(len(move_tree))
        print 'time: {} secs per move'.format((end-start)/len(move_tree))


    #def test_timing(self):
    #    import time
    #    import cProfile
    #    profile = cProfile.Profile()
    #
    #    test_board =   ('rnbqkbnr\n' #8
    #                    '.......p\n' #7
    #                    '..pppQ..\n' #6
    #                    '.pPP.PN.\n' #5
    #                    '.PB.....\n' #4
    #                    'p....PP.\n' #3
    #                    'P.....P.\n' #2
    #                    'RNB.K..R')  #1
    #    position=new_game(test_board)
    #
    #    start = time.time()
    #    profile.enable()
    #
    #    for i in xrange(10):
    #        position.get_moves()
    #
    #    profile.disable()
    #
    #    end = time.time()
    #    profile.print_stats(sort="time")
    #
    #    print end - start


