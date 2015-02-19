import multiprocessing as mp

from serializers import PositionSerializer




class MinimaxLookahead(object):
    """"Basic Minimax (with Alpha/Beta) look-ahead"""

    @classmethod
    def evaluate(cls, position, colour=None, *args, **kwargs):
        raise NotImplementedError





    @classmethod
    def breadth_search(cls, position, depth):

        with open('dump1.txt','rb') as old_file:
            old_data = old_file.readlines()

        old_data_dict = dict((ln.strip().split(';')[0],ln.strip().split(';')[2]) for ln in old_data)



        with open('dump2.txt','a') as f:

            # Temp
            from pystockfish import Engine
            eng = Engine(depth=15)

            from ai.basic import ShannonAI
            unexplored = [(position, 0)]
            explored = []
            while unexplored:
                new_position, new_depth = unexplored.pop(0)



                fen = PositionSerializer.to_fen(new_position)

                if fen not in old_data_dict:
                    eng.setfenposition(fen)

                    best_move = eng.bestmove()['move']

                    line = '{0};{1};{2}\n'.format(fen,str(new_depth), best_move)

                    f.write(line)
                    f.flush()

                evaluation = ShannonAI.evaluate(new_position)
                explored.append((new_position, new_depth, evaluation))
                if new_depth < depth:
                    moves = new_position.get_moves()
                    for move in moves:
                        unexplored.append((move, new_depth+1))

            return explored

    cache = {}

    @classmethod
    def get_moves(cls, position):

        # fen = PositionSerializer.to_fen(position)
        # if fen not in cls.cache:
        #     cls.cache[fen] = position.get_moves()
        # else:
        #     print position, len(cls.cache)
        #
        # return cls.cache[fen]

        return position.get_moves()

    @classmethod
    def get_best_move(cls, position, depth=3):
        return cls.alpha_beta_get_best_move(position, depth)


    @classmethod
    def alpha_beta_get_best_move(cls, position, depth=3):
        """Minimax with Alphabeta"""
        ret = min(cls.get_moves(position), key=lambda new_position: cls.alphabeta_helper(new_position, depth-1, float('-Inf'), float('+Inf')))
        return ret

    @classmethod
    def alphabeta_helper(cls, position, depth, alpha, beta):

        if depth == 0:
            return cls.evaluate(position)

        moves = cls.get_moves(position)

        if len(moves)==0:
            return cls.evaluate(position)



        if depth % 2 == 1:
            for move in moves:
                alpha = max(alpha, cls.alphabeta_helper(move, depth-1, alpha, beta))
                if beta <= alpha:
                    break
            return alpha

        else:
            for move in moves:
                beta = min(beta, cls.alphabeta_helper(move, depth-1, alpha, beta))
                if beta <= alpha:
                    break
            return beta

