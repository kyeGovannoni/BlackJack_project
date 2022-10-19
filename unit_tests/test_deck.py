
import sys
sys.path.append('/home/kye/Documents/projects_/backjack_lw/blackjack/core_game')

import unittest
from blackjack.core_game.shuffle import ShuffleDeckLw, card_total, TestDeck


class ShoeCountTest(unittest.TestCase):

    def test_6_deck_shoe(self):
        six_shoe_shuffler = ShuffleDeckLw(decks = 6)
        shoe = six_shoe_shuffler()
        self.assertEqual(len(tuple(shoe)), 6*52)

    def test_1_deck_shoe(self):
        six_shoe_shuffler = ShuffleDeckLw(decks = 1)
        shoe = six_shoe_shuffler()
        self.assertEqual(len(tuple(shoe)), 52)


class ShoeShuffleTest(unittest.TestCase):
    
    def test_compare_two_shoes(self):
        # A higher number of decks will reduce the change of random matches.
        ten_shoe_shuffler = ShuffleDeckLw(decks = 10)
        shoe_one = ten_shoe_shuffler()
        shoe_two = ten_shoe_shuffler()

        self.assertFalse(tuple(shoe_one) == tuple(shoe_two))


class CardTotalsTestCase(unittest.TestCase):

    def test_hand_ace_value_total(self):
        cards =  ['A',9]
        self.assertEqual(card_total(cards), 20)
    
    def test_hand_ace_face_total(self):
        cards =  ['A','J']
        self.assertEqual(card_total(cards), 21)

    def test_hand_ace_bust_total(self):
        cards =  ['A',10,10,5]
        self.assertEqual(card_total(cards), 22) # if ace and all bust defaults to 22.

    def test_hand_face_total(self):
        cards =  ['K','J']
        self.assertEqual(card_total(cards), 20)

    def test_hand_face_bust_total(self):
        cards =  ['K','J','Q']
        self.assertEqual(card_total(cards), 30)

    def test_hand_no_face(self):
        cards =  [6, 9]
        self.assertEqual(card_total(cards), 15)

    def test_ace_hand_combination(self):
        cards = [ 'A', 5, 'A']
        self.assertEqual(card_total(cards), 17)


if __name__ =='__main__':
    unittest.main()