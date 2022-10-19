from itertools import count, islice
from shuffle import  ShuffleDeckLw
from players import Player, Hand, Dealer, DealersHand
from basicstrategy import basic_strategy_hard_totals 

class Game:
    '''
    To initalise a game please include the player objects (dealer, player) and a game object (shuffler).
    
    The game handles the rules, the players, Split plays, the deck and the balances/payouts. 

    A clock is used to keep track of the players turn.
    Balance is used to deduct bets, allows for split plays and deactivate players from the next round who's balance is 0.
    The move logic is also validated through the Game class.
    '''

    valid_moves = ['hit','stand','double','split','bust']
    payout = {'return':3, 'bet':2}

    def __init__(self, dealer: Player, players : Player, shuffler : ShuffleDeckLw, deck_pen = 1):    
        self.dealer = dealer
        self.players = players      
        self.shuffler = shuffler 
        self.next_player = None
        #has the round come to an end?
        self.round_end = False
        #cards drawn from the shoe.
        self.drawn = 0
        #how far into the shoe will the game go before the round ends?
        self.deck_pen = deck_pen 
        #deck/shoe for this round.
        self.deck = self.shuffler()

    def _next_player_index(self):
        #create a clock that will keep track of player order using modulus.
        return next(self.clock) % self.counter

    def draw_card(self, n = 1):
        #draw n numbers of cards for the shoe/deck.
        self.drawn += n
        return list(islice(self.deck, n))
    
    def deal(self):
        #reset game attributes.
        self._new_game()
        
        #Give the dealer a new hand with 2 cards.
        self.dealer.hand = DealersHand(self.draw_card(2), self.dealer)
        
        #deal out 2 cards to each player.
        for _ in range(self.counter):
            p = self._next_player_index()
            self.players[p].hand = Hand(
                                    cards = self.draw_card(2),
                                    bet = self.players[p].bet,
                                    owner = self.players[p]
                                    )
        
        self.current_player = self._next_player_index()

        if self.dealer.blackjack or max(p.blackjack for p in self._active_players):
            self._black_jack()
    
    def _black_jack(self):
        if self.dealer.hand.blackjack:
            for player in self._active_players: 
                for hand in player.hand:
                    hand.wait = True

        if not self.dealer.hand.blackjack:
            for player in self._active_players:
                for hand in player.hand:
                    if hand.blackjack: 
                        self._player_outcome_win(hand, hand.blackjack)
                        hand.wait = True
        self.next_round()     

 
    def _new_game(self):
        '''
        Starts a new round. 
        Creates a new shoe, checks if the players have enough in their balance to move to the next round, if not they are made inactive.
        Clears the hands of the players and the dealers.
        Resets the clock.
        Draws players cards.
        '''
         #reset dealer attributes.
        self.dealer.clear_hand()
        #reset player attributes.
        for player in self.players:
            player.clear_hand()
        #Get players.
        a_players = list(filter(lambda x:x if x.balance > 0 else None, self.players))  
        if len(a_players) == 0:
            raise AttributeError("Not enough active players!")
        self._active_players = a_players
        ## need to add up split bets to the player index when they occur.
        self._player_bets = [player.bet for player in a_players]
        #reset game attributes.
        self.clock = count(0,1)
        self.counter = len(self.players)   
        self.round_end = False
        if self.drawn >= (self.shuffler.shoe * self.deck_pen):
            print(self.drawn)
            self.drawn = 0 
            self.deck = self.shuffler()
    
    @property
    def round_over(self): 
        if all(p.wait for p in self._active_players) and self.dealer.wait:
            print('Round over.')
            return True

        if self.dealer.bust:
            print('Dealer bust!')
            return True
    
    def next_round(self):
        if not self.round_over:

            if all(p.wait for p in self._active_players):
                self._make_move(self.dealer.hand, is_dealer=True)

            if self._active_players[self.current_player].wait:
                #if player has made all their moves, get next player.
                self.current_player = self._next_player_index()

            elif self._active_players[self.current_player].ready:
                # player is ready.
                c_player = self._active_players[self.current_player]
                #validate player moves.
                if self.__valid_moves(c_player):
                    # iterate through hand moves.
                    if not c_player.bust and not c_player.wait: 
                        for hand in c_player.hand:
                            self._make_move(hand)           
                else: print('Not all players have entered a valid move.') 
               
        if self.round_over:
            self._rebalance()
            return True

    @classmethod
    def __valid_moves(cls, player):        
        if all(p.next_move in cls.valid_moves for p in player.hand if not p.bust):
            return True   
        return False         

    def _rebalance(self):
        #iterate through all active non bust players.
        for player in filter(
                        lambda x: x if not x.bust else False, 
                        self._active_players 
                        ):

            for hand in player.hand:
                
                if not self.dealer.bust and self.dealer.hand() >= 17: 
                # dealer not bust and hand total is over or equal to 17.
                    if hand() == self.dealer.hand():
                        pass
                    if hand() < self.dealer.hand():
                        self._player_outcome_loss(hand)

                    if hand() > self.dealer.hand():
                        self._player_outcome_win(hand, hand.blackjack)
    
                if self.dealer.bust:
                    #dealer bust.
                    self._player_outcome_win(hand, hand.blackjack )
    
    @classmethod
    def _player_outcome_loss(cls, hand):
        hand.owner.balance -= hand.bet
        hand.bet = 0

    @classmethod
    def _player_outcome_win(cls, hand, blackjack):
        if blackjack:
            hand.owner.balance += ((hand.bet) * cls.payout['return']) / cls.payout['bet']
        else:
            hand.owner.balance += hand.bet
        hand.bet = 0

    def _make_move(self,hand, is_dealer = False):          
      if hand.next_move == 'hit': self._hit(hand)
      elif hand.next_move == 'stand': self._stand(hand)
      elif hand.next_move == 'double': self._double(hand)
      elif hand.next_move == 'split': self._split(hand)

    def _hit(self, hand):
        hand.cards = self.draw_card()
        hand.next_move = None
        if hand.bust and hand.owner != self.dealer: self._player_outcome_loss(hand)

    def _double(self, hand):
        if len(hand.cards) == 2:
            hand.bet += hand.bet
            hand.cards = self.draw_card()
            hand.next_move = None
            hand.wait = True
            if hand.bust: self._player_outcome_loss(hand)
       
    def _stand(self, hand):
        hand.wait = True
        hand.next_move = None

    def _split(self, hand):
        ## check the player has enough in their balance before creating a new hand.
        if hand.cards[0] == hand.cards[1] and len(hand.cards) == 2:
            hand.owner.hand = Hand(
                                cards = [self.draw_card(1), hand.cards.pop()],
                                bet   = hand.owner.bet,
                                owner = hand.owner
                                )
            hand.cards = self.draw_card()
            

class MainGame(Game):
    def __init__(self, dealer, players, shuffler, deck_pen = 1):    
        super().__init__(dealer=dealer,players=players,shuffler=shuffler, deck_pen=deck_pen)
        self.deal()
##-------------------------------------------------------------------------------------------------
class SplitGame(MainGame):
    def _new_game(self):
        self.deck = self.shuffler

