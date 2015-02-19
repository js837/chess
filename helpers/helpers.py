from position import Position, WHITE, BLACK
from pieces import King, Rook, Knight, Bishop, Queen, Pawn


def new_game(board_str = None):
    """Creates a new game based on text representation"""
    mappings = {'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King, 'P': Pawn}

    position = Position()
    if board_str is None:
        # White plays North
        board_str = (' rnbqkbnr\n' #8
                     ' pppppppp\n' #7
                     ' ........\n' #6
                     ' ........\n' #5
                     ' ........\n' #4
                     ' ........\n' #3
                     ' PPPPPPPP\n' #2
                     ' RNBQKBNR')  #1
                     # abcdefgh

    # Permute the board so that Top left become bottom left
    board_str = board_str.replace(' ', '').replace('\n','')
    ranks = reversed([board_str[i:i+8] for i in range(0, 64, 8)])
    board_str = ''.join(ranks)

    board = ()
    rank = ()
    for piece in board_str:
        if piece == '.':
            rank += (None,)
        elif piece.isupper():
            rank += (mappings[piece.upper()](WHITE), )
        elif piece.islower():
            rank += (mappings[piece.upper()](BLACK), )
        if len(rank) == 8:
            board += (rank,)
            rank = ()

    position.board=board
    return position

