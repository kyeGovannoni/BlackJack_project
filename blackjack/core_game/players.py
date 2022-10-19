from shuffle import card_total


class Player:
    ''' The Player class represents a player in the game of black jack. 
        It it initalised with a balance amount and a base bet. 
        The player class is coupled with the hand class, as such hand fuction can be called through the 
        player class. 

        The player must have a high enough balance to meet the current games betting requirments.

        A player can become inactive to miss a game.

      '''
    def __init__(self, balance, bet):
        self.bet = bet
        self._balance = balance
        self.active = True
        self._hands = []

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount > 0:
            self._balance = amount
    
    @property
    def hand(self):
        return self._hands
           
    @hand.setter
    def hand(self, hand):
    # add a card through the players Hand instance. 
        self._hands.append(hand)
        
    def clear_hand(self):
        self._hands = []
    
    #Player round statuses.
    @property
    def ready(self):
        return all(hand.next_move for hand in self._hands)
   
    @property
    def wait(self):
        return all(hand.wait for hand in self._hands)
    
    @property
    def bust(self):
        return all(hand.bust for hand in self._hands)

    @property
    def blackjack(self):
        return bool(max([h.blackjack for h in self._hands] ))
    

class Dealer(Player):
    ''' 
    A dealer is a sub class of Player but does not require an balance amount or bet, if one is provided it will be ignored.
        
    '''
    def __init__(self):
        # no balance or bet is passed.
        super().__init__(None, None)

    @property
    def hand(self):
        return self._hands
           
    @hand.setter
    def hand(self, hand):
    # a dealer may only have one hand.
        if len(self._hands) == 0:
            self._hands = hand
    
    @property
    def bust(self):
        return self._hands.bust      
   
    @property
    def wait(self):    
        return self._hands.wait     

    @property
    def blackjack(self):    
        return self._hands.blackjack


class Hand():
    '''
    The hand is what manages the cards, this includes if the hand is considered bust, a black jack 
    and any status updates of the hand. 

    The "moves" or status are tied to a hand rather than a player so that a player may have 
    multiple hands.
    
    It holds the cards.

    A player can have many hands but a hand can only have one owner (Player).
    '''
    def __init__(self, cards, bet, owner):
        self._cards = cards
        self.bet  = bet
        self._owner = owner
        self._move = None
        self.bust = False
        self._wait = False
        self.blackjack = self.blackjack()
        

    def __repr__(self):
        return f'{type(self).__name__}(cards = {self.cards})'
    
    def __str__(self):
        return f'{card_total(self._cards)}'
    
    def __call__(self):
        return card_total(self._cards)
    
    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, card):
        self._cards.append(card)
        if card_total(self._cards) > 21:
            self.bust = True

    @property
    def next_move(self):
        return self._move

    @next_move.setter
    def next_move(self, move):
        self._move = move
    
    @property
    def wait(self):
        return self.bust if self.bust else self._wait
    
    @wait.setter
    def wait(self, Bool):
        self._wait = bool(Bool)

    @property
    def owner(self):
        return self._owner

    def blackjack(self):
    #Tests if hand is a black jacks, if so set hand action to wait.
        if len(self._cards) == 2 and card_total(self._cards) == 21:
            self._wait = True
            return True
        return False


class DealersHand(Hand):
    '''
    A dealers hand is a sub class of Hand, however it is different as it must follow a set of game rules.
    '''

    def __init__(self, cards, owner):
        super().__init__(cards,None, owner)
        self.next_move = None

    @property
    def next_move(self):
        return self._move

    @next_move.setter
    def next_move(self, move ):
    #Determines if the hands next move is to hit or stand.
        if card_total(self.cards) <= 17:
            self._move = 'hit'
        else: self._move = 'stand'