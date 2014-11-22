

class MinimaxLookahead(object):
    """" Provides basic function for lookahead"""

    @classmethod
    def evaluate(cls, position, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_best_move(cls, position, depth=3):
        return min(position.get_moves(), key=lambda new_position: cls.get_best_helper(new_position, depth-1))

    @classmethod
    def get_best_helper(cls, position, depth):
        if depth == 0:
            return cls.evaluate(position)

        elif depth % 2 == 1:
            moves = position.get_moves()
            # Choose the worst possible move for the opponent
            return min((cls.get_best_helper(new_position, depth=depth-1) for new_position in moves))
        else:
            moves = position.get_moves()
            # Choose the best possible move for me
            return max((cls.get_best_helper(new_position, depth=depth-1) for new_position in moves))

