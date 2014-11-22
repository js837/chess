from algorithms import MinimaxLookahead
from pieces import King, Queen, Bishop, Knight, Rook, Pawn

class AI(object):

    @classmethod
    def get_best_move(cls, position, *args, **kwargs):
        raise NotImplementedError


class EvaluationFunction(object):
    """
    Subclasses must implement eval. This returns a float showing strength of position.
    """

    @classmethod
    def evaluate(cls, position, colour=None, *args, **kwargs):
        raise NotImplementedError




