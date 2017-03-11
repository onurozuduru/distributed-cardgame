import random

import flask
from flask import Flask
from flask import abort


#### Player ####
from flask import send_from_directory


class Player:
    __STATUS__ = ("OFFLINE", "ONLINE")

    def __init__(self, deck, name):
        self.hand = random.sample(deck, 3)
        self.name = name
        self.moves = []
        self.points = 0
        self.status = self.__STATUS__[0]

    def clear(self, deck):
        self.hand = random.sample(deck, 3)
        self.moves = []
        self.points = 0
        self.make_offline()

    def move(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.moves.append(card)
            return card
        return None

    def last_move(self):
        if self.moves:
            return self.moves[-1]
        return None

    def add_point(self):
        self.points += 1

    def make_online(self):
        self.status = self.__STATUS__[1]

    def make_offline(self):
        self.status = self.__STATUS__[0]

    def is_online(self):
        return self.status == self.__STATUS__[1]

    def get_object(self):
        return {'name': self.name,
                'hand': self.hand,
                'moves': self.moves,
                'points': self.points}
########


#### Game ####
class Game:
    __STAGES__ = ("NEW", "CONTINUE", "END")
    __PLAYER_NAMES__ = ("p1", "p2")
    __TOTAL_ROUNDS__ = 3

    def __init__(self):
        self.deck = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.players = self._init_players()
        self.round = 0
        self.stage = self.__STAGES__[0]
        self.current_player = None

    def get_object(self):
        curr = None
        if self.current_player:
            curr = self.current_player.get_object()
        return {'round': self.round,
                'stage': self.stage,
                'current_player': curr}
    def reset(self):
        self.round = 0
        self.stage = self.__STAGES__[0]
        self.current_player = None
        for player in self.players:
            player.clear(self.deck)

    def _init_players(self):
        return [Player(self.deck, self.__PLAYER_NAMES__[0]),
                Player(self.deck, self.__PLAYER_NAMES__[1])]

    def _is_everyone_inside(self):
        for player in self.players:
            if not player.is_online():
                return False
        return True

    def who_is_missing(self):
        for player in self.players:
            if not player.is_online():
                return player
        return None

    def register_player(self, p_name):
        if p_name in self.__PLAYER_NAMES__:
            p_index = self.__PLAYER_NAMES__.index(p_name)
            self.players[p_index].make_online()

    def begin(self):
        if self._is_everyone_inside():
            self.stage = self.__STAGES__[1]
            self.current_player = self.players[0]
            return True
        return False

    def is_round_end(self):
        return len(self.players[0].hand) == len(self.players[1].hand)

    def next_player(self):
        if self.current_player:
            for i, player in enumerate(self.players):
                if self.current_player.name == player.name:
                    self.current_player = self.players[1-i]
                    return self.current_player
        return None

    def new_round(self):
        if not self._is_everyone_inside():
            return None
        self.round += 1
        player_index = self.round % 2
        self.current_player = self.players[player_index]

        if self.round == self.__TOTAL_ROUNDS__:
            self.stage = self.__STAGES__[2]
            return self.stage, self.winner()
        return self.stage, self.current_player

    def end_of_round(self):
        opp_index = self.round % 2
        cur_move = self.current_player.last_move()
        opp_move = self.players[opp_index].last_move()
        if not cur_move or not opp_move:
            return
        if len(self.current_player.moves) != len(self.players[opp_index].moves):
            return
        if cur_move == opp_move:
            self.current_player.add_point()

    def winner(self):
        p1 = self.players[0]
        p2 = self.players[1]
        if p1.points == p2.points:
            return None
        if p1.points > p2.points:
            return p1
        return p2
########

#### App ####

app = Flask(__name__)

games = []


def someone_needs_player():
    for i, g in enumerate(games):
        if g.stage == g.__STAGES__[0]:
            missing = g.who_is_missing()
            if missing:
                return i, missing
    return None


def get_player_by_name(game, p_name):
    for player in game.players:
        if p_name == player.name:
            return player
    return None


@app.route('/newgame')
def new_game():
    res = {}
    missing = someone_needs_player()
    if missing:
        missing[1].make_online()
        res['game_num'] = missing[0]
        res['player'] = missing[1].get_object()
        if not games[missing[0]].begin():
            abort(404)
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
    if game_num >= len(games):
        abort(404)
    game = games[game_num]
    res = {}
    if player_name in game.__PLAYER_NAMES__:
        player = get_player_by_name(game, player_name)
        m = player.move(move)
        if m:
            if game.is_round_end():
                game.end_of_round()
                stage, player = game.new_round()
                res['stage'] = stage
                if (stage == game.__STAGES__[2]) and (not player):
                    res['player'] = 'NO_ONE'
                else:
                    res['player'] = player.get_object()
            else:
                p = game.next_player()
                if not p:
                    abort(404)
                res['stage'] = game.stage
                res['player'] = p.get_object()
            res['last_move'] = m
    return flask.jsonify(res)


@app.route('/game/<int:game_num>/newround')
def new_round(game_num):
    if game_num >= len(games):
        abort(404)
    game = games[game_num]
    res = game.new_round()
    if not res:
        abort(404)
    stage, player = res[0], res[1]
    return flask.jsonify({'stage': stage, 'player': player.get_object()})


@app.route('/game/<int:game_num>/endofround')
def end_round(game_num):
    if game_num >= len(games):
        abort(404)
    game = games[game_num]
    game.end_of_round()
    return flask.jsonify(game.get_object())


@app.route('/game/<int:game_num>/winner')
def who_won(game_num):
    if game_num >= len(games):
        abort(404)
    game = games[game_num]
    winner = game.winner()
    res = {}
    if not winner:
        res['is_winner'] = 0
        res['winner'] = 'NO_ONE'
    else:
        res['is_winner'] = 1
        res['winner'] = winner.get_object()
    return flask.jsonify(res)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


if __name__ == '__main__':
    app.run()
