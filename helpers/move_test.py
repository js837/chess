from games.masters import games
from position.serializers import PositionSerializer, MoveSerializer
import pprint

lines = []
python_objs = []

for i, (fen, best_move) in enumerate(games):

    if i%8==0:
        print '{0}%'.format(float(i)/len(games) * 100)

    position = PositionSerializer.from_fen(fen)

    moves = tuple(MoveSerializer.to_str(move.last_move) for move in position.get_moves())
    str_moves = ','.join(moves)

    line = '{0};{1};{2}'.format(fen, best_move, str_moves)

    lines.append(line)

    python_objs.append((fen, best_move, moves))


with open('moves_test.txt', 'wb') as f:
    f.write('\n'.join(lines))


with open('python_moves_test.txt', 'wb') as g:
    g.write(pprint.pformat(python_objs))
