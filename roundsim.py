from game import Dealer, Player
from game import MainGame
from shuffle import ShuffleDeckLw, card_total
from basicstrategy import basic_strategy_hard_totals




p = Player(100,5)
p2 =Player(100,5)
d = Dealer()

g = MainGame(players=[p],dealer= d,shuffler= ShuffleDeckLw(decks=6), deck_pen = 0.85)
for i in range(1000):
    print('players balance',p.balance)
    while not p.wait:
        for i in p.hand:
            print('hand total',i())
            print('dealer up card', d.hand.cards[0])
            try:
                
                if d.hand.cards[0] in ('J','Q','K'):
                    upc = 10 
                else: upc = d.hand.cards[0]

                a = basic_strategy_hard_totals[upc][i()]
                print(a)
                i.next_move='double' if a =='D' and len(i.cards) == 2 else 'hit'
                if a =='S': i.next_move='stand'
                if a =='H': i.next_move='hit'


            except KeyError:
                if i() < 8:
                    i.next_move = 'hit'
                    print('H')
                if i() > 17:
                    i.next_move = 'stand'
                    print('S')

            g.next_round()

    while not d.wait:
        g.next_round()
    print('dealers hand' ,d.hand)
    print('players hand' ,p.hand[0]())
    print('players balance',p.balance)
    print('\n')
    g.deal()