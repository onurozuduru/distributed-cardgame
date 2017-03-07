import requests
import random

name = ''
game_number = -1
hand = []
moves= []
points = 0

HOST="http://localhost"
PORT="5000"


def begin_game():
    rq=requests.get("{1}:{2}{3}".format(HOST,PORT,"/newgame"))

    if rq.status_code==200:
        resp=rq.json()
        game_number=resp['game_num']

        player=resp['player']
        name=player['name']
        hand=player['hand']
        moves=player['moves']
        points=player['points']
        
        return True
    return False


def make_move(move):
   
    rq=requests.get("{1}:{2}{3}{4}{5}/{6}".format(HOST,PORT,"/move/",game_number,name,move))

    if rq.status_code==200:
       return rq.json()
    return None
    


def check_game():
    rq=requests.get("{1}:{2}{3}{4}".format(HOST,PORT,"/game/",str(game_number)))
    if rq.status_code==200:
        return rq.json()
    return None



def run():
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