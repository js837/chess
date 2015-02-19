import re
import sys
from collections import Counter

from .general import new_game
from position.serializers import PositionSerializer, MoveSerializer

import logging

LOG_FILENAME = 'logging_example2.out'
logging.basicConfig(filename=LOG_FILENAME,  level=logging.DEBUG)

"""
PGN Parser
"""

"""[Event "It"]
[Site "Enghien les Bains FRA"]
[Date "2003.06.22"]
[Round "9"]
[White "Adams, Michael"]
[Black "Akopian, Vladimir E"]
[Result "1/2-1/2"]
[WhiteElo "2723"]
[BlackElo "2703"]
[ECO "C07"]
[EventDate "2003.06.13"]

1.e4 e6 2.d4 d5 3.Nd2 c5 4.exd5 Qxd5 5.Ngf3 cxd4 6.Bc4 Qd6 7.Qe2 Nf6 8.Nb3
Nc6 9.Bg5 Qb4+ 10.Bd2 Qb6 11.O-O-O Bd7 12.Bg5 Bc5 13.Kb1 O-O-O 14.Ne5 Nxe5
15.Qxe5 Bd6 16.Qe2 h6 17.Bd2 Bb4 18.Bxb4 Qxb4 19.Nxd4 Kb8 20.f4 Qc5 21.Nf3
Ng4 22.Rd4 Bc8 23.Rhd1 Rxd4 24.Nxd4 e5 25.h3 exd4 26.hxg4 Bxg4 27.Qxg4 .
Qxc4 28.Qxg7 Rc8 29.Qe5+ Ka8 30.Qe4 a6 31.b3 Qc6 32.Qxc6 Rxc6 33.f5 Rd6
34.Kc1 Ka7 35.Kd2 Kb6 36.Re1 Rd8 37.g4 Rg8 38.Re4 Kc5 39.Kd3 h5 40.gxh5
Rg3+ 41.Kd2 Rh3 42.f6 Rxh5 43.Re7 Rf5 44.Rxf7 b5 45.Rf8 Kc6 46.Kd3 Rf4 47.
a3 Kc7 48.a4 Kb6 49.Ke2 Rf5 50.Kd3 Rf4 51.axb5 axb5 52.c3 dxc3 53.Kxc3 Kc6
54.b4 Kc7 55.f7 Kb7 56.Kd3 Rf3+ 57.Ke4 Rf1 58.Ke5 Rf2 59.Ke6 Re2+ 60.Kd6
Rf2 61.Kc5 1/2-1/2"""



if __name__ == '__main__':


    lines = []

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if len(sys.argv) > 3:
        max_games = int(sys.argv[3])
    else:
        max_games = None

    with open(input_file) as f:
        pgn_games_str = f.read()
    pgn_games_str = re.sub(r'\[.+?\]', '', pgn_games_str)

    pgn_games = re.split('\n{2,}', pgn_games_str)


    for game_num, game in enumerate(pgn_games):

        if not game:
            continue

        if max_games is not None and game_num > max_games:
            break

        game = game.replace('\n',' ')
        moves = re.split(r'\s{1,}', game)

        position = new_game()
        print('{}/{}'.format(str(game_num), str(len(pgn_games))))

        for move in moves:
            move = re.sub(r'\d+\.', '', move)
            if not move or move in ('1-0', '0-1', '1/2-1/2'):
                break

            from_fen = PositionSerializer.to_fen(position)
            pgn_moves = position.get_pgn_moves()


            try:
                position = pgn_moves[move]
            except KeyError:
                try:
                    position = pgn_moves[move.replace('e.p.','')]
                except KeyError:
                    for key in pgn_moves:
                        if key.replace('e.p.','') == move:
                            position = pgn_moves[key]
                            break
                        if key.replace('+','#') == move:
                            position = pgn_moves[key]
                            break
                    else:
                        logging.debug('Error at game {} in file {}'.format(str(game_num), input_file))
                        logging.debug(str(list(pgn_moves.keys())))
                        logging.debug(str(move))
                        logging.debug(str(moves))
                        logging.debug(from_fen)
                        logging.debug('----------------------------------')
                        break


            move_str = MoveSerializer.to_str(position.last_move)

            line = '{},{}'.format(from_fen, move_str)
            lines.append(line)

    with open(output_file, 'wb') as output:
        output.write('\n'.join(lines))










