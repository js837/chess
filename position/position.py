from collections import defaultdict, namedtuple

from helpers.coord import *
from helpers.coord import get_rank_file


WHITE, BLACK = True, False  # So can easily flip between colours
DRAW = 0.5


class Position(object):
    def __init__(self, board=None, active_colour=WHITE, castling='KQkq', en_passant=None,
                 last_move=None, half_move=0, full_move=1, white_king_coord=None, black_king_coord=None):

        self.board = board or ((None,)*8,)*8
        self.active_colour = active_colour
        self.castling = castling
        self.en_passant = en_passant
        self.last_move = last_move
        self.half_move = half_move
        self.full_move = full_move

        self.white_king_coord = None
        self.black_king_coord = None

        # Find the Kings
        from pieces import King
        if self.white_king_coord is None or self.black_king_coord is None:
            for piece, coord in self.iter_pieces():
                if isinstance(piece, King):
                    if piece.colour is WHITE:
                        self.white_king_coord = coord
                    else:
                        self.black_king_coord = coord

    def __getitem__(self, coord):
        """ For simplicity allow the syntax: `position[coord]` to get piece at coord"""
        return self.board[coord[0]][coord[1]]

    def __eq__(self, other):
        return self.board == other.board and \
               self.active_colour==other.active_colour and \
               self.castling==other.castling and \
               self.en_passant==other.en_passant and \
               self.last_move==other.last_move and \
               self.half_move==other.half_move and \
               self.full_move==other.full_move

    def __str__(self):
        from pieces import Piece
        piece_list = []
        for i, rank in enumerate(reversed(self.board)):
            for j, piece in enumerate(rank):
                if piece is None:
                     piece_short_name = Piece.short_name
                else:
                    piece_short_name = piece.short_name if piece.colour is WHITE else piece.short_name.lower()
                piece_list.append(piece_short_name)

            piece_list.append( '|%s\n' % str(9-int(get_rank_file((i,j))[1])))
        return '--------\n' + ''.join(piece_list) + '--------\n' + 'abcdefgh\n'

    def to_html(self):
        from jinja2 import Template
        from IPython.display import HTML
        with open('templates/../templates/position.html') as f:
            position_template = Template(f.read())
        return HTML(position_template.render(position=self))

    def iter_pieces(self):
        # Iterate through all pieces on board
        for i, rank in enumerate(self.board):
            for j, piece in enumerate(rank):
                yield piece, Coord(i,j)

    def in_check(self, colour):

        """ Decide if this position is in check for this colour (by iterating away from the king) """
        from pieces import King, Queen, Bishop, Knight, Rook, Pawn

        king_coord = self.white_king_coord if colour is WHITE else self.black_king_coord
        if king_coord is None:
            return False

        for piece_class in King, Queen, Bishop, Knight, Rook, Pawn:
            dummy_piece = piece_class(colour = colour)
            for coord_to in dummy_piece.iter_move_coords(self, king_coord):
                piece = self[coord_to]
                if isinstance(piece, piece_class) and piece.colour != colour:
                    return True


        return False

    def get_moves_and_result(self, colour=None):
        if colour is None:
            colour = self.active_colour

        moves = self.get_moves(colour)
        result = None

        if not moves:
            if self.in_check(colour):  # Result
                result = not colour
            else:  # Stalemate
                result = DRAW
        return moves, result

    def get_moves(self, colour=None):
        if colour is None:
            colour = self.active_colour
        moves = tuple()
        for piece, coord in self.iter_pieces():
            if piece is not None and piece.colour == colour:
                for move in piece.get_moves(self, coord):
                    if not move.in_check(colour):
                        moves += (move,)
        return moves

    def get_pgn_moves(self, colour=None):
        """Give the PGN notation for this move"""
        if colour is None:
            colour = self.active_colour

        destintation_dict = defaultdict(tuple)
        ret = dict()

        ## Build a destination dict to check for ambiguous moves.



        for new_position in self.get_moves(colour):
            coord_to = new_position.last_move.coord_to
            piece = type(self[new_position.last_move.coord_from])


            destintation_dict[(coord_to, piece)] += (new_position,)
        
        for coord_to, piece in destintation_dict.keys():
            # Check for ambigious moves
            if len(destintation_dict[coord_to, piece]) == 1:
                ambiguity = 'NONE'
            else:
                ranks = [position.last_move.coord_from[1] for position in destintation_dict[(coord_to, piece)]]
                files = [position.last_move.coord_from[0] for position in destintation_dict[(coord_to, piece)]]
                if len(ranks) == len(set(ranks)):
                    ambiguity = 'RANK'
                elif len(files) == len(set(files)):
                    ambiguity = 'FILE'
                else:
                    ambiguity = 'BOTH'

            # Loop through moves and print notation for moves
            for position in destintation_dict[coord_to, piece]:
                notation = self.get_notation_for_move(position, colour, ambiguity=ambiguity)
                ret[notation] = position

        return ret

    def get_notation_for_move(self, position, colour, ambiguity=''):
        from pieces import King, Pawn

        # Castling
        move=position.last_move

        # If there is a pawn promotion then this move is not ambigous
        if move.new_piece_class:
            ambiguity = 'NONE'

        # Special case of castling
        if isinstance(self[move.coord_from], King) and move.coord_from[1] == 4:
            check = '+' if position.in_check(not colour) else ''
            if move.coord_to[1] == 6:
                castling_str = 'O-O'
                return '{}{}'.format(castling_str, check) # Kingside
            if move.coord_to[1] == 2:
                castling_str = 'O-O-O'
                return '{}{}'.format(castling_str, check) # Queenside


        en_passant_flag = isinstance(self[move.coord_from], Pawn) and self.en_passant == move.coord_to
        # For en passant captures always specify file of departure
        if en_passant_flag:
            ambiguity = 'RANK'
            capture_coord = move.coord_to + self.step_back
        else:
            capture_coord = move.coord_to


        # When a pawn makes a capture, the file from which the pawn departed is used to identify the pawn
        if isinstance(self[move.coord_from], Pawn) and self[capture_coord]:
            ambiguity = 'RANK'


        # Deal with ambiguity with coord_to
        if ambiguity == 'NONE':
            amb = ''
        elif ambiguity == 'RANK':
            amb = get_rank_file(move.coord_from)[0]
        elif ambiguity == 'FILE':
            amb = get_rank_file(move.coord_from)[1]
        elif ambiguity == 'BOTH':
            amb = get_rank_file(move.coord_from)

        return '%(name)s%(amb)s%(capture)s%(rankfile)s%(promotion)s%(en_passant)s%(check)s' % \
            {
                'name': self[move.coord_from].algebraic_name,
                'amb': amb,
                'capture': 'x' if self[capture_coord] else '',
                'rankfile': get_rank_file(move.coord_to),
                'promotion': '={}'.format(move.new_piece_class.algebraic_name) if move.new_piece_class else '',
                'en_passant': 'e.p.' if en_passant_flag else '',
                'check': '+' if position.in_check(not colour) else '',
            }

    def move_piece(self, coord_from, coord_to, new_piece_class=None, en_passant_capture_coord=None):
        """Return a copy of the board"""

        old_piece = self[coord_from]
        if new_piece_class:
            piece = new_piece_class(old_piece.colour)
        else:
            piece = old_piece

        board = self.board

        # If en-passant then must remove captured pawn.
        if en_passant_capture_coord:
            board = self._insert_piece(board, en_passant_capture_coord, None)

        # Insert the piece at coord_to
        board = self._insert_piece(board, coord_to, piece)

        # Remove the piece at coord_from
        board = self._insert_piece(board, coord_from, None)

        return board

    @classmethod
    def _insert_piece(cls, board, coord, piece):
        """ Return a new board with piece inserted at coord"""
        rank = board[coord[0]][:coord[1]] + (piece,) + board[coord[0]][coord[1]+1:]
        return board[:coord[0]] + (rank,) + board[coord[0]+1:]

    def is_empty_square(self, coord):
        # Maybe should integrate this into get item?

        return is_valid_sqaure(coord) and not(self[coord])

    @property
    def step_back(self):
        return S if self.active_colour is WHITE else N




class Move(object):
    """
    Holds information for board to make a move.
    """
    def __init__(self, coord_from, coord_to, new_piece_class=None):

        # Compulsory info
        self.coord_from = coord_from
        self.coord_to = coord_to
        self.new_piece_class = new_piece_class



    def __eq__(self, other):
        return self.coord_from == other.coord_from and \
               self.coord_to==other.coord_to and \
               self.new_piece_class is other.new_piece_class




