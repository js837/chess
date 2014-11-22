from position import *
from pieces import *
from helpers.coord import *


class Piece(object):
    # Idea: Consider making this not abstract and represent a blank piece?
    moves = tuple()
    short_name = '.'
    algebraic_name = '.'
    unicode_html = '&#9812;'

    many = False

    def __init__(self, colour=WHITE):
        self.colour = colour


    def get_new_position(self, position, coord_from, coord_to, en_passant=None, new_piece=None, castling=None):
        """ Generate a new position for move: coord_from --> coord_to"""

        # En-passant logic, slightly messy...
        en_passant_flag = isinstance(position[coord_from], Pawn) and position.en_passant == coord_to
        if en_passant_flag:
            capture_coord = coord_to + position.step_back
        else:
            capture_coord = coord_to




        captured_piece = position[capture_coord]
        piece = type(position[coord_from])
        active_colour = position.active_colour


        # Update King coordinate
        white_king_coord = position.white_king_coord
        black_king_coord = position.black_king_coord
        if isinstance(position[coord_from], King):
            if position[coord_from].colour is WHITE:
                white_king_coord = coord_to
            else:
                black_king_coord = coord_to

            king_coord = coord_to


        last_move = Move(coord_from, coord_to, piece, active_colour, capture=False, en_passant_flag=en_passant_flag,
                         new_piece=new_piece, check=False)
        if castling is None:
            castling = position.castling
            # Note: last_move.en_passant is a boolean flag specifying if last move was en_passant capture.


        new_board = position.move_piece(coord_from, coord_to, new_piece, en_passant_capture_coord=capture_coord)
        active_colour = not position.active_colour




        half_move = position.half_move
        if not (captured_piece and captured_piece.colour != self.colour or piece is Pawn):
            half_move += 1
        else:
            half_move = 0

        full_move = position.full_move
        if position.active_colour == BLACK:
            full_move += 1

        return Position(new_board, active_colour, castling, en_passant, last_move, half_move, full_move, white_king_coord, black_king_coord)

    def iter_move_coords(self, position, coord):
        """
        Generator for coordinates of all possible moves for this piece
        """
        for move in self.moves:
            coord_to = coord + move

            while Position.is_valid_sqaure(coord_to):

                captured_piece = position[coord_to]

                # Hit our own piece (this is not a valid move)
                if captured_piece and captured_piece.colour == self.colour:
                    break

                yield coord_to

                # Cannot make multiple moves eg. if we are not a Bishop, Rook, Queen
                if not self.many:
                    break

                # Captured opponent piece (this is a valid move but we can't continue in this direction
                if captured_piece and captured_piece.colour != self.colour:
                    break

                coord_to = coord_to + move

    def get_moves(self, position, coord, castling=None):
        """ Get new positions for all possible moves for this piece
        @param position:
        @param coord:
        """
        ret = tuple()

        for coord_to in self.iter_move_coords(position, coord):
            new_position = self.get_new_position(position, coord, coord_to, castling=castling)
            ret += (new_position,)

        return ret


class Pawn(Piece):
    short_name = 'P'
    algebraic_name = ''
    html_white = '&#9817;'
    html_black = '&#9823;'


    # TODO: Unify this method and the logic in get_moves()
    def iter_move_coords(self, position, coord):
        take_left = NE if self.colour == WHITE else SE
        take_right = NW if self.colour == WHITE else SW

        for move in (take_left, take_right):
            coord_to = coord + move
            if Position.is_valid_sqaure(coord_to):
                captured_piece = position[coord_to]
                # There must be a piece at i_to capture
                if captured_piece and (captured_piece.colour != self.colour):
                    yield coord_to


    def get_moves(self, position, coord):
        moves = tuple()
        #coord = self.get_coord(position)

        # After single move and capture we need to check for promotion
        # Maybe method make_move should be on the piece, so can be overridden

        # Need to reset half move counter
        # Need to reset en_passant

        # Define some relative values
        if self.colour is WHITE:
            step1, step2 = N, N2
            take_left, take_right = NE, NW
            first_line, final_line = 1, 7
        else:
            step1,step2 = S, S2
            take_left, take_right = SE, SW
            first_line, final_line = 6, 0

        # Single Move
        coord_new = coord + step1
        if position.is_empty_square(coord_new):
            # Promotion
            if coord_new[0] == final_line:
                for piece_class in Rook, Bishop, Knight, Queen:
                    new_piece = piece_class(self.colour)
                    new_position = self.get_new_position(position, coord, coord_new, new_piece=new_piece)
                    moves += (new_position,)
            else:
                new_position = self.get_new_position(position, coord, coord_new)
                moves += (new_position,)

        # Double move
        coord_new = coord + step2
        if position.is_empty_square(coord_new) \
            and coord[0] == first_line \
            and position.is_empty_square(coord + step1):

            new_position = self.get_new_position(position, coord, coord_new, en_passant=(coord + step1))
            moves += (new_position,)

        # Capture
        for move in (take_left, take_right):
            # There must be a piece at i_to capture or en-passent
            coord_to = coord + move
            if Position.is_valid_sqaure(coord_to):
                captured_piece = position[coord_to]
                if position.en_passant == coord_to or (captured_piece and (captured_piece.colour != self.colour)):
                    new_position = self.get_new_position(position, coord, coord_to)
                    moves += (new_position,)




        return moves



class King(Piece):
    short_name = 'K'
    algebraic_name = 'K'
    html_white = '&#9812;'
    html_black = '&#9818;'
    moves = (N, E, S, W, NE, SE, SW, NW)

    def _get_castling_move(self, position, king_coord, rook_coord, new_castling_str):
        sign = +1 if king_coord[1] < rook_coord[1] else -1

        if isinstance(position[king_coord], King) and isinstance(position[rook_coord], Rook):
            # Check for pieces between Rook and Kings
            for i in xrange(rook_coord[1]-sign, king_coord[1], -sign):
                if position[(king_coord[0],i)]:
                    return

            # Move one step to check for Check
            step = self.get_new_position(position, king_coord, (king_coord[0], king_coord[1]+sign*1), castling=new_castling_str)
            if not step.in_check(self.colour):
                castle_move = self.get_new_position(position, rook_coord, (king_coord[0],king_coord[1]+sign*1), castling=new_castling_str)
                full_castle_move = self.get_new_position(castle_move, king_coord, (king_coord[0],king_coord[1]+sign*2), castling=new_castling_str)
                full_castle_move.active_colour = not position.active_colour
                return full_castle_move

    def get_moves(self, position, coord):
        """Include castling logic"""

        white_castling_str = ''.join([x for x in position.castling if x.isupper()])
        black_castling_str = ''.join([x for x in position.castling if x.islower()])

        # If King moves then it loses ability to castle
        if self.colour is WHITE:
            castling_rank = 0
            castling_str = white_castling_str
            new_castling_str = black_castling_str
        else:
            castling_rank = 7
            castling_str = black_castling_str
            new_castling_str = white_castling_str

        moves = super(King, self).get_moves(position, coord, castling=new_castling_str)

        # Prevent castling out of Check.
        if position.in_check(self.colour):
            return moves

        if 'K' in castling_str.upper():
            king_coord, rook_coord = (castling_rank,4), (castling_rank,7)
            castle_move = self._get_castling_move(position, king_coord, rook_coord, new_castling_str)
            if castle_move:
                moves += (castle_move,)

        if 'Q' in castling_str.upper():
            king_coord,rook_coord  = (castling_rank,4), (castling_rank,0)
            castle_move = self._get_castling_move(position, king_coord, rook_coord, new_castling_str)
            if castle_move:
                moves += (castle_move,)

        return moves


class Rook(Piece):
    many = True
    short_name = 'R'
    algebraic_name = 'R'
    html_white = '&#9814;'
    html_black = '&#9820;'
    moves = (N, E, S, W)

    def get_moves(self, position, coord):

        # If this rook is moving from it's starting position then remove the relevant castling ability
        castling = position.castling
        if self.colour is WHITE:
            if coord == (0,0):
                castling = position.castling.replace('Q','')
            elif coord == (0,7):
                castling = position.castling.replace('K','')
        else:
            if coord == (7,0):
                castling = position.castling.replace('q','')
            elif coord == (7,7):
                castling = position.castling.replace('k','')

        return super(Rook, self).get_moves(position, coord, castling=castling)


class Knight(Piece):
    short_name = 'N'
    algebraic_name = 'N'
    html_white = '&#9816;'
    html_black = '&#9822;'
    moves = (N + NE, N + NW, E + NE, E + SE, S + SE, S + SW, W + SW, W + NW)


class Bishop(Piece):
    many = True
    short_name = 'B'
    algebraic_name = 'B'
    html_white = '&#9815;'
    html_black = '&#9821;'
    moves = (NE, SE, SW, NW)


class Queen(Piece):
    many = True
    short_name = 'Q'
    algebraic_name = 'Q'
    html_white = '&#9813;'
    html_black = '&#9819;'
    moves = (N, E, S, W, NE, SE, SW, NW)
