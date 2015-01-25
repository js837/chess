from ai.metrics import EvaluationFunction, AI, MinimaxLookahead
from serializers import PositionSerializer
from pieces import King, Queen, Bishop, Knight, Rook, Pawn



PIECE_MASK = (
    (0,1,2,3,3,2,1,0),
    (1,2,3,4,4,3,2,1),
    (2,3,4,5,5,4,3,2),
    (4,5,6,7,8,6,5,4),
    (4,5,6,7,8,6,5,4),
    (2,3,4,5,5,4,3,2),
    (1,2,3,4,4,3,2,1),
    (0,1,2,3,3,2,1,0),
)


class ShannonAI(MinimaxLookahead, EvaluationFunction, AI):


    @classmethod
    def evaluate(cls, position, colour=None, *args, **kwargs):
        """ Basic Shannon Eval function as below ###
        # 2000*(K-K')
        # + 90*(Q-Q')
        # + 50*(R-R')
        # + 30*(B-B' + N-N')
        # + 10*(P-P')

        # - 5*(D-D' + S-S' + I-I')
        # + 1*(M-M') + ..."""


        if colour is None:
            colour = position.active_colour

        rank = 0 # num_moves

        check = position.in_check(not colour)
        if check:
            rank = float('-Inf')

        for piece, coord in position.iter_pieces():
            sign = 1 if piece and colour== piece.colour else -1
            piece_class = type(piece)

            weight = 0
            # if piece:
            #     weight = PIECE_MASK[coord[0]][coord[1]]
            # else:
            #     weight = 0

            if piece_class is King:
                weight += 2000
            elif piece_class is Queen:
                weight += 90
            elif isinstance(piece, Bishop):
                weight += 50
            elif isinstance(piece, Knight):
                weight += 30
            elif isinstance(piece, Rook):
                weight += 30
            elif isinstance(piece, Pawn):
                weight += 10
            elif piece is None:
                weight += 0
            rank += weight * sign

            #num_legal_moves_diff = len(self.get_moves(self.active_colour)) - len(self.get_moves(not self.active_colour))
            #rank += 0.1 * num_legal_moves_diff

        return rank