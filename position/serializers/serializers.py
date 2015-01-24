from helpers.coord import get_rank_file, get_coord_from_rank_file
from position import Position, Move
from pieces import King, Rook, Knight, Bishop, Queen, Pawn, WHITE, BLACK



class PositionSerializer(object):
    mappings = {'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King, 'P': Pawn}

    @classmethod
    def to_fen(cls, position):
        board_str_list = []
        for i, rank in enumerate(reversed(position.board)):
            blank_count = 0
            for j, piece in enumerate(rank):
                if piece is None:
                    blank_count += 1
                else:
                    if blank_count > 0:
                        board_str_list.append(str(blank_count))
                    blank_count = 0
                    piece_short_name = piece.short_name if piece.colour is WHITE else piece.short_name.lower()
                    board_str_list.append(piece_short_name)
            if blank_count > 0:
                board_str_list.append(str(blank_count))
            if i<7:
                board_str_list.append('/')

        board_str = ''.join(board_str_list)
        active_colour_str = 'w' if position.active_colour is WHITE else 'b'
        castling_str = position.castling or '-'
        en_passant_str = get_rank_file(position.en_passant) if position.en_passant else '-'
        half_move_str = str(position.half_move)
        full_move_str = str(position.full_move)

        return ' '.join([board_str, active_colour_str, castling_str, en_passant_str, half_move_str, full_move_str])


    @classmethod
    def from_fen(cls, fen_str):
        # Separate the 6 components
        board_str, active_colour_str, castling_str, en_passant_str,\
           half_move_str, full_move_str = fen_str.strip().split(' ')

        position = Position()

        # Construct the board
        board = tuple()
        for rank_str in board_str.split('/'):
            rank = tuple()
            for piece_str in rank_str:
                if piece_str in '12345678':
                    # Blanks
                    rank += (None,) * int(piece_str)
                else:
                    # Piece
                    piece_colour = WHITE if piece_str.isupper() else BLACK
                    rank += (cls.mappings[piece_str.upper()](piece_colour),)
            board = (rank,) + board

        # Rest of Properties
        position.board = board
        position.active_colour = WHITE if active_colour_str=='w' else BLACK
        position.castling = '' if castling_str is '-' else castling_str
        position.en_passant = None if en_passant_str=='-' else get_coord_from_rank_file(en_passant_str)
        position.half_move = int(half_move_str)
        position.full_move = int(full_move_str)

        return position


class MoveSerializer(object):

    @classmethod
    def to_str(cls, move):
        coord_from_str = get_rank_file(move.coord_from)
        coord_to_str = get_rank_file(move.coord_to)
        new_piece_class_str = move.new_piece_class.algebraic_name if move.new_piece_class else '-'
        return '{}/{}/{}'.format(coord_from_str, coord_to_str, new_piece_class_str)

    @classmethod
    def from_str(cls, move_str):
        coord_from_str, coord_to_str, new_piece_class_str = move_str.split('/')

        coord_from = get_coord_from_rank_file(coord_from_str)
        coord_to = get_coord_from_rank_file(coord_to_str)
        if new_piece_class_str == '-':
            new_piece_class = None
        else:
            new_piece_class = PositionSerializer.mappings[new_piece_class_str] # Is this an instance?
        return Move(coord_from, coord_to, new_piece_class)