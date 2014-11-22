from pieces import King, Queen, Bishop, Knight, Rook, Pawn
from serializers import PositionSerializer
from ai.metrics import EvaluationFunction, AI, MinimaxLookahead




class ShannonAI(MinimaxLookahead, EvaluationFunction, AI):


    @classmethod
    def evaluate(cls, position, colour=None, *args, **kwargs):
        """ Basic Shannon Eval function as below ###
        # 200*(K-K')
        # + 9*(Q-Q')
        # + 5*(R-R')
        # + 3*(B-B' + N-N')
        # + 1*(P-P')

        # - 0.5*(D-D' + S-S' + I-I')
        # + 0.1*(M-M') + ..."""

        if colour is None:
            colour = position.active_colour

        rank = 0 # num_moves

        check = position.in_check(not colour)
        if check:
            rank = float('-Inf')

        for piece, coord in position.iter_pieces():
            sign = 1 if piece and colour== piece.colour else -1
            piece_class = type(piece)

            # Weight centre of board higher
            x_weight = 3-abs(coord[0]-3)
            y_weight = 3-abs(coord[1]-3)

            weight = x_weight + y_weight

            if piece_class is King:
                weight += 200

            elif piece_class is Queen:
                weight += 9
            elif isinstance(piece, Bishop):
                weight += 5
            elif isinstance(piece, Knight):
                weight += 3
            elif isinstance(piece, Rook):
                weight += 3
            elif isinstance(piece, Pawn):
                weight += 1
            elif piece is None:
                weight += 0
            rank += weight * sign

            #num_legal_moves_diff = len(self.get_moves(self.active_colour)) - len(self.get_moves(not self.active_colour))
            #rank += 0.1 * num_legal_moves_diff

        return rank