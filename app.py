import uuid
import datetime

from flask import Flask, render_template, session, request, jsonify

from position import WHITE, BLACK, DRAW
from serializers import PositionSerializer
from ai.basic import ShannonAI

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yx R~XHH!jmN]LWX/,?RT'


@app.route("/get-moves", methods=['POST'])
def get_moves():
    fen = request.json['fen']
    ai = request.json['ai']



    position = PositionSerializer.from_fen(fen)
    new_fen = None

    if ai:
        position = ShannonAI.get_best_move(position, depth=2)
        new_fen = PositionSerializer.to_fen(position)

    moves, result = position.get_moves_and_result()
    result_str = {
        WHITE: 'W',
        BLACK: 'B',
        DRAW: '1/2',

    }.get(result, '')

    move_dicts = []
    for new_position in moves:
        move = new_position.last_move
        move_dict = {
                        'from': move.coord_from,
                        'to': move.coord_to,
                        'newPiece': move.new_piece_class,
                        'fen': PositionSerializer.to_fen(new_position),
                        'score': ShannonAI.evaluate(new_position),
                        'colour': new_position.active_colour,
                    }
        move_dicts.append(move_dict)

    move_dicts.sort(key=lambda x:x['score'])



    return jsonify({
        'fen': fen,
        'ai': ai,
        'new_fen': new_fen,
        'result': result_str,
        'moves': move_dicts,
        'colour': position.active_colour,
        'score': ShannonAI.evaluate(position),
        'from': position.last_move.coord_from if position.last_move else None,
        'to': position.last_move.coord_to if position.last_move else None,
    })


@app.route("/", methods=['GET', 'POST'])
def main():
    utc_now = datetime.datetime.utcnow()
    return render_template('main.html', time=utc_now)


if __name__ == "__main__":
    app.run(debug=True)
