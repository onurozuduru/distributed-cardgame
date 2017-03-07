import random

import flask
from flask import Flask
from flask import abort

from game import Game

app = Flask(__name__)

games = []

def someone_needs_player():
    for i, g in enumerate(games):
        if g.stage == g.__STAGES__[0]:
            missing = g.who_is_missing()
            if missing:
                return i, missing
    return None


@app.route('/newgame')
def new_game():
    res = {}
    missing = someone_needs_player()
    if missing:
        missing[1].make_online()
        res['game_num'] = missing[0]
        res['player'] = missing[1].get_object()
    else:
        game = Game()
        games.append(game)
        game_num = len(games) - 1
        player = game.players[0]
        player.make_online()
        res['game_num'] = game_num
        res['player'] = player.get_object()
    return flask.jsonify(res)


@app.route('/game/<int:game_num>')
def game_status(game_num):
    if game_num >= len(games):
        abort(404)
    return flask.jsonify(games[game_num].get_object())


@app.route('/move/<int:game_num>/<player_name>/<move>')
def make_move(game_num, player_name, move):
    pass


@app.route('/game/<int:game_num>/winner')
def who_won(game_num):
    pass



@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
