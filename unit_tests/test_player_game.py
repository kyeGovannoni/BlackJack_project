import unittest
import sys
sys.path.append('/home/kye/Documents/projects_/backjack_lw/blackjack/core_game')

from blackjack.core_game.players import Dealer, Player, Hand, DealersHand
from blackjack.core_game.game import MainGame
from blackjack.core_game.shuffle import ShuffleDeckLw, card_total, TestDeck


class PlayerAttrTestCase(unittest.TestCase):

    def setUp(self):   
        self.player = Player(100, 5)

    def test_player_add_cards(self):
        hand = Hand(['J','K'],5, self.player)
        self.assertEqual(hand.cards, ['J','K'])

    def test_player_clear_hand(self):
        self.player.hand =  Hand(['J','K'],5, self.player)
        self.player.clear_hand()
        self.assertEqual(self.player.hand, [])
    
    def test_player_bust(self):
        hand = Hand(['K','J'],5, self.player)
        hand.cards = 'K'

        self.assertTrue(hand.bust)
        self.assertTrue(self.player.wait)

    def test_dealer_move_hit(self):
        dealer = Dealer()
        dealer.hand = DealersHand([2,2], owner=dealer)
        self.assertEqual(dealer.hand.next_move,'hit')
    
    def test_dealer_move_stand(self):
        dealer = Dealer()
        dealer.hand = DealersHand([10,6], owner=dealer)
        self.assertEqual(dealer.hand.next_move,'hit')
     


class GameRoundsTestCase(unittest.TestCase):

    def setUp(self):   
        self.p1 = Player(100,5)
        self.p2 = Player(100,10)
        self.p3 = Player(100,5)
        self.p4 = Player(100,5)
        self.players = [self.p1 ,self.p2, self.p3, self.p4]
        self.shuffler = ShuffleDeckLw()
        self.dealer = Dealer()
        self.game = MainGame(players=self.players, dealer = self.dealer, shuffler = self.shuffler)

    def test_all_players_hand_drawn(self):
        self.assertTrue(all([ len(p.hand[0].cards) == 2 for p in self.players ]))

    def test_all_players_hand_new_round(self):     
        self.game.deal()  
        self.assertEquals(
                sum([len(p.hand[0].cards) for p in self.players]) + len(self.dealer.hand.cards),
                10)

    def test_next_player_turn(self):
        c = self.game._next_player_index()
        self.assertEquals(self.players[c], self.game._active_players[c] )

    def test_game_inital_pot(self):
        self.assertEquals(sum(self.game._player_bets), 25)


class PlayerMovesTest(unittest.TestCase):
    def setUp(self):   
        self.p1 = Player(100,5)
        self.players = [self.p1]
        self.dealer = Dealer()
        self.game = MainGame(players=self.players, dealer = self.dealer, shuffler =ShuffleDeckLw())

    def test_player_hit(self):
        self.p1.hand[0].next_move ='hit'
        self.game.next_round()
        self.assertEqual(len(self.p1.hand[0].cards), 3)
        self.assertEqual(self.p1.bet,5)

    def test_player_stand(self):
        self.p1.hand[0].next_move ='hit'
        self.game.next_round()
        self.assertIn(len(self.p1.hand[0].cards),[3,2])
        self.assertEqual(self.p1.bet,5)

    def test_player_double(self):
        self.p1.hand[0].next_move ='double'
        self.game.next_round()
        self.assertEqual(len(self.p1.hand[0].cards), 3)
        self.assertIn(self.p1.hand[0].bet,[10,0])

    def test_player_split(self):
        self.p1.clear_hand()
        self.p1.hand = Hand(['A','A'], 5, self.p1)
        self.p1.hand[0].next_move ='split'
        self.game.next_round()
        self.assertEqual(len(self.p1.hand[0].cards), 2)
        self.assertEqual(len(self.p1.hand[1].cards), 2)
        self.assertEqual(len(self.p1.hand), 2)
    
    def test_player_hit_after_double(self):
        self.p1.hand[0].next_move ='double'
        self.game.next_round()
        total = card_total(self.p1.hand[0].cards)
        self.p1.hand[0].next_move ='hit'
        self.game.next_round()
        self.assertEqual(len(self.p1.hand[0].cards), 3)
        self.assertEqual(card_total(self.p1.hand[0].cards), total)



class GameRulesTest(unittest.TestCase):
    def setUp(self):   
        self.p1 = Player(100,5)
        self.players = [self.p1]
        self.dealer = Dealer()
        self.game = MainGame(players=self.players, dealer = self.dealer, shuffler =ShuffleDeckLw())

    def test_dealer_stand_false(self):
        self.dealer.next_move ='stand'
        self.game.next_round()
        self.assertFalse(self.dealer.wait)

   

class GameRulesBlackJackTest(unittest.TestCase):

    def setUp(self):
         
        self.d1 = Dealer()
        self.p1 = Player(100,10)
        self.g1 = MainGame(players = [self.p1], dealer = self.d1, shuffler = TestDeck(['A','J',10,9]))

        self.d2 = Dealer()
        self.p2 = Player(100,10)
        self.g2 = MainGame(players = [self.p2], dealer = self.d2, shuffler = TestDeck([10,9,'A','J']))

    def test_dealer_blackjack(self):  
        self.assertTrue(self.d1.blackjack)

    def test_dealer_blackjack_wait(self):
        self.assertTrue(self.d1.wait)

    def test_dealer_blackjack_player_wait(self):
        self.assertTrue(self.p1.wait)

    def test_dealer_blackjack_player_balance(self):
        self.assertEqual(self.p1.balance, 90)
    
    def test_dealer_blackjack_round_over(self):
        self.assertTrue(self.g1.round_over)

    def test_player_blackjack(self):  
        self.assertTrue(self.p2.blackjack)

    def test_player_blackjack_wait(self):
        self.assertTrue(self.p2.wait)

    def test_player_blackjack_dealer_wait(self):
        self.assertTrue(self.d2.wait)

    def test_player_blackjack_round_over(self):
        self.assertTrue(self.g2.round_over)

    def test_player_blackjack_dealer_balance(self):
        self.assertEqual(self.p2.balance, 115)
       


class ClassGameOutcomesTest(unittest.TestCase):

    def setUp(self):   
        self.p1 = Player(100,5)
        self.players = [self.p1]
        self.dealer = Dealer()
        self.deck = TestDeck([10, 5, 10, 10])
        self.game = MainGame(players=self.players, dealer = self.dealer, shuffler = self.deck )

    def test_outcome_push(self):
        self.p1.next_move ='stand'
        self.game.next_round()
        self.dealer.next_move ='stand'
        self.game.next_round()
        self.p1.next_move ='stand'
        self.game.next_round()
        #self.assertTrue(self.game.round_end)
        self.assertTrue(self.p1.wait)
        #self.assertTrue(self.dealer.wait)
        #self.assertFalse(self.p1.bust)
        #self.assertFalse(self.dealer.bust)
        #self.assertEqual(self.p1.balance, 100)

    def test_dealer_stand_false(self):
        self.dealer.clear_hand()
        self.dealer.hand = DealersHand([10, 5] , self.dealer)

        self.p1.next_move ='stand'
        self.game.next_round()
        self.dealer.next_move = 'stand'
        self.game.next_round()
        self.assertTrue(card_total(self.dealer.hand),15)
        self.assertFalse(self.dealer.wait)
        self.assertFalse(self.game.round_end)

    def test_outcome_player_bust(self):
        self.p1.next_move ='hit'
        self.assertTrue(self.game.next_round())
        self.assertTrue(self.p1.bust)
        self.assertFalse(self.dealer.bust)
        self.assertEqual(self.p1.balance, 95)
    
    def test_outcome_dealer_bust(self):
        self.p1.next_move ='stand'
        self.game.next_round()
        self.dealer.next_move ='hit'
        self.assertTrue(self.game.next_round())
        self.assertTrue(self.dealer.bust)
        self.assertFalse(self.p1.bust)
        self.assertEqual(self.p1.balance, 105)
    




    



if __name__ =='__main__':
    unittest.main()