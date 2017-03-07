from player import Player


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
        opp_index = 1 - (self.round % 2)
        cur_move = self.current_player.last_move()
        opp_move = self.players[opp_index].last_move()
        if cur_move == opp_move:
            self.players[opp_index].add_point()

    def winner(self):
        p1 = self.players[0]
        p2 = self.players[1]
        if p1.points == p2.points:
            return None
        if p1.points > p2.points:
            return p1
        return p2


