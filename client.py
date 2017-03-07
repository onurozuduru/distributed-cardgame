from time import sleep

import requests


class Client:
    __STAGES__ = ("NEW", "CONTINUE", "END")
    __WAIT_TIME__ = 15

    def __init__(self):
        self.name = ''
        self.game_number = -1
        self.hand = []
        self.moves = []
        self.points = 0
        self.HOST = "http://localhost"
        self.PORT = "5000"

    def begin_game(self):
        rq = requests.get("{0}:{1}{2}".format(self.HOST, self.PORT, "/newgame"))

        if rq.status_code == 200:
            resp = rq.json()
            self.game_number = resp['game_num']
            player = resp['player']
            self.name = player['name']
            self.hand = player['hand']
            self.moves = player['moves']
            self.points = player['points']
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
                                                    str(self.game_number), "/winner"))
        if rq.status_code == 200:
            return rq.json()
        return None

    def is_valid_move(self, move):
        return move in self.hand

    def run(self):
        if not self.begin_game():
            print 'Could not begin game.'
            return

        game_status = self.check_game()
        if not game_status:
            print 'Server seems to be down...'
            return

        print "You are the %s" % self.name
        if game_status['stage'] == self.__STAGES__[0]:
            print "Waiting other player to join the game..."
            stage = game_status['stage']
            while stage == self.__STAGES__[0]:
                sleep(self.__WAIT_TIME__)
                game_status = self.check_game()
                stage = game_status['stage']
        print "Everyone is online... Let's play a game..."

        game_status = self.check_game()
        stage = game_status['stage']
        current_player = None
        if stage == self.__STAGES__[1]:
            current_player = game_status['current_player']
        round = game_status['round']
        while stage == self.__STAGES__[1]:
            print "Round %s" % str(round)
            if current_player and current_player['name'] == self.name:
                self.hand = current_player['hand']
                print "Your hand is %s" % str(self.hand)

                user_move = raw_input("Please make a move: ")
                while not self.is_valid_move(user_move):
                    print "Your move %s is not a valid move!" % user_move
                    user_move = raw_input("Please make a move: ")

                move_res = self.make_move(user_move)
                if not move_res:
                    print "Something went wrong!"
                    return

                stage = move_res['stage']
                if stage == self.__STAGES__[2]:
                    break
                current_player = move_res['player']
                #TODO check round is changed (if not wait other player)
                #TODO update round
                #TODO get other player's move
            #TODO else: wait other player
        #TODO after game is done check who is winner


if __name__ == '__main__':
    Client().run()
