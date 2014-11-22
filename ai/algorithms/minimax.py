import multiprocessing as mp

class MinimaxLookahead(object):
    """"Basic Minimax (with Alpha/Beta) look-ahead"""

    @classmethod
    def evaluate(cls, position, colour=None, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def breadth_search(cls, position, depth):
        unexplored = [(position, 0)]
        explored = []
        while unexplored:
            new_position, new_depth = unexplored.pop()
            explored.append((new_position, new_depth))
            if new_depth < depth:
                moves = new_position.get_moves()
                for move in moves:
                    unexplored.append((move, new_depth+1))

        return explored

    @classmethod
    def get_best_move(cls, position, depth=3):
        """Minimax with Alphabeta"""
        ret = min(position.get_moves(), key=lambda new_position: cls.alphabeta_helper(new_position, depth-1, float('-Inf'), float('+Inf')))
        return ret

    @classmethod
    def alphabeta_helper(cls, position, depth, alpha, beta):

        if depth == 0:
            return cls.evaluate(position)

        moves = position.get_moves()

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

