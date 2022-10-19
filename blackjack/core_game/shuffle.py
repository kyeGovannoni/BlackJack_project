import random
from itertools import combinations


class ShuffleDeckLw:
    '''
    The shuffler object can generate shuffled shoes based on the values passed when initalised.
    The returned iterable is a generator object that is exhuastable. Calling the shuffler again will produce a new shoe. 
    
    The shuffler can also assess an iterable of cards to determine their value based on the rules of blackjack.
    
    eg a hand of A, A, 10 would be 12 not 32. Like wise a hand of A, A, 8 wound be 20, 11 + 1 + 8.
    *this functionality should be move out of the shuffle class. 
    
    '''
    cards = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
    deck = 52

    def __init__(self, decks = 1):
        if decks < 1: 
            raise ValueError('No of decks must be greater than 1.')

        self.decks = int(decks)
        self.shoe = ShuffleDeckLw.deck * decks

    def __call__(self):
        return self._shuffle()
    
    def _shuffle(self): 
        def _mapp_cards(n):    
            v = n % len(ShuffleDeckLw.cards)
            return ShuffleDeckLw.cards[v]

        order = random.sample(
                    range(ShuffleDeckLw.deck * self.decks), (ShuffleDeckLw.deck * self.decks)
                    )
        return map(_mapp_cards, order)
  
#Logic to determine hand total, there are a few values the hand could be depending on the circumstances. 
def card_total(hand):       
        if 'A' in hand:
            aces = len([card for card in hand if card == 'A'])           
           #sums of all ace combinations
            a_comb = set(map(
                    sum,
                    combinations(
                        [1]*aces + [11]*aces,
                        aces
                        )
                    ))
            other_cards = [(lambda card:card if isinstance(card,int) else 10)(card) for card in hand if card != 'A']
            totals = list(map(
                            lambda x: x + sum(other_cards),
                            a_comb
                            ))
            try:
                return max(filter(lambda t:t if t <=21 else False, totals) )
            except ValueError:
               return  22
            ## if both totals are bust >21 then return 22
        else:
            return sum(map(lambda x : x if isinstance(x,int) else 10, hand))


class TestDeck:
            shoe = 1
            def __init__(self, cards):
                self.shoe = 1 
                self.deck_ = cards 

            def __call__(self):
                for c in self.deck_:
                    yield c



