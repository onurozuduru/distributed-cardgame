import random


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
