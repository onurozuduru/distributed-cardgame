import requests
import random

class Client:
    def __init__(self):
        self.name = ''
        self.game_number = -1
        self.hand = []
        self.moves = []
        self.points = 0
        self.HOST="http://localhost"
        self.PORT="5000"

    def begin_game(self):
        rq = requests.get("{0}:{1}{2}".format(self.HOST, self.PORT, "/newgame"))

        if rq.status_code == 200:
            resp=rq.json()
            self.game_number=resp['game_num']
            player=resp['player']
            self.name=player['name']
            self.hand=player['hand']
            self.moves=player['moves']
            self.points=player['points']
            return True
        return False

    def make_move(self, move):
        rq = requests.get("{0}:{1}{2}{3}/{4}/{5}".format(self.HOST, self.PORT,
                                                       "/move/", str(self.game_number),
                                                       self.name, move))
        if rq.status_code == 200:
            return rq.json()
        return None

    def check_game(self):
        rq = requests.get("{0}:{1}{2}{3}".format(self.HOST, self.PORT, "/game/",
                                               str(self.game_number)))
        if rq.status_code == 200:
            return rq.json()
        return None

    def get_winner(self):
        rq = requests.get("{0}:{1}{2}{3}{4}".format(self.HOST, self.PORT, "/game/",
                                                 str(self.game_number),"/winner"))
        if rq.status_code == 200:
            return rq.json()
        return None

    def run(self):
        # new game req
        # check status
        # make sure you are the current player
        # make a move
        # check status
        # if needed wait second player
        # otherwise check who won the round
        # check game is finished
        # loop me
        pass

        if not begin_game():
            print 'could not begin game'
            return


        game_status=check_game()
        if not game_status:
            print 'Server seems to be down... really??'
            return

        card=random.sample(hand,1)
        while card in moves:
            card=random.sample(hand,1)

        moves.append(card)

        make_move(card)

       

        
        

if __name__ == '__main__':
    pass