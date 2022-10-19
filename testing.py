from shuffle import ShuffleDeckLw
from players import Player, Hand

player = Player(100,5)
deck = ShuffleDeckLw()()

#player.hand = 
print( Hand([next(deck),next(deck)]))
player.hand = Hand([next(deck),next(deck)], bet = player.bet)
player.hand = Hand([next(deck),next(deck)])
player.hand = Hand([next(deck),next(deck)])

print(player.hand)
print(player.hand[0].bet)
print(player.ready)