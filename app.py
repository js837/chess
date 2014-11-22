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
    fen = request.form.get('fen')
    ai = request.form.get('ai')
    position = PositionSerializer.from_fen(fen)
    if ai:
        position = ShannonAI.get_best_move(position, depth=3)
        new_fen = PositionSerializer.to_fen(position)

    moves, result = position.get_moves_and_result()
    result_str = None
    if result is WHITE:
        result_str = 'W'
    elif result is BLACK:
        result_str = 'B'
    elif result is DRAW:
        result_str = '1/2'


    move_dicts = []
    for new_position in moves:
        move = new_position.last_move
        move_dict = {
                        'from': move.coord_from,
                        'to': move.coord_to,
                        'newPiece': move.new_piece,
                        'fen': PositionSerializer.to_fen(new_position),
                    }
        move_dicts.append(move_dict)
    return jsonify(fen=fen,ai=ai,new_fen=new_fen,result=result_str, moves=move_dicts)


@app.route("/", methods=['GET', 'POST'])
def main():
    utc_now = datetime.datetime.utcnow()
    return render_template('main.html', time=utc_now)


if __name__ == "__main__":
    app.run(debug=True)
