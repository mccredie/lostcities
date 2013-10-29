
import unittest

from . import gameproxybase
from . import gamestate
from . import deck

class GameProxyBaseTests(unittest.TestCase):
    class_under_test = gameproxybase.GameProxyBase
    def test_hand_attribute_returns_copy_of_players_hand(self):
        p1 = 1
        g = gamestate.GameState()
        p1_hand = g.hands[p1][:] = [('r', 1), ('r', 2), ('w', 3), ('b', 4)]

        p = self.class_under_test(g, p1)
        proxy_hand = p.hand

        self.assertSequenceEqual(p1_hand, proxy_hand)
        self.assertIsNot(p1_hand, proxy_hand)
        

    def test_discards_attribute_returns_set_of_top_discards(self):
        p1 = 1
        g = gamestate.GameState()
        g.discards['r'][:] = [('r', x) for x in [1,2,3,4]]
        g.discards['g'][:] = [('g', x) for x in [5,6,7,8]]
        g.discards['b'][:] = [('b', x) for x in [9,10,11,12]]
        g.discards['w'][:] = [('w', x) for x in [13,14,15,16]]
        g.discards['y'][:] = [('y', x) for x in [17,18,19,20]]

        expected = frozenset([
                ('r', 4), ('g', 8), ('b', 12), ('w', 16), ('y', 20)])

        p = self.class_under_test(g, p1)

        self.assertEqual(expected, p.discards)


    def test_discards_attribute_returns_set_of_top_discards_sans_empty(self):
        p1 = 1
        g = gamestate.GameState()
        g.discards['r'][:] = []
        g.discards['g'][:] = [('g', x) for x in [5, 6, 7, 8]]
        g.discards['b'][:] = [('b', x) for x in [9, 10, 11, 12]]
        g.discards['w'][:] = [('w', x) for x in [13, 14, 15, 16]]
        g.discards['y'][:] = [('y', x) for x in [17, 18, 19, 20]]

        expected = frozenset([('g', 8), ('b', 12), ('w', 16), ('y', 20)])

        p = self.class_under_test(g, p1)

        self.assertEqual(expected, p.discards)


    def test_adventures_returns_dict_of_adventure_piles(self):
         p1 = 1
         g = gamestate.GameState()
         p = self.class_under_test(g, p1)

         g.hands[p1][:] = [('r', 2), ('g', 3), ('b', 4)]
         g.play(p1, 0)
         g.play(p1, 0)
         g.play(p1, 0)

         expected = {'r': [('r', 2)], 'g': [('g', 3)],
                 'b': [('b', 4)], 'w':[], 'y': []}

         self.assertEqual(expected, p.adventures)
         self.assertIsNot(g.adventures[p1], p.adventures)
         for a in p.adventures:
             self.assertIsNot(g.adventures[p1][a], p.adventures[a])

    def test_other_adventures_returns_other_player_adventure_piles(self):
         p0 = 0
         p1 = 1

         g = gamestate.GameState()
         p = self.class_under_test(g, p0)

         g.hands[p1][:] = [('r', 2), ('g', 3), ('b', 4)]
         g.play(p1, 0)
         g.play(p1, 0)
         g.play(p1, 0)

         expected = {'r': [('r', 2)], 'g': [('g', 3)], 
                 'b': [('b', 4)], 'w': [], 'y': []}

         self.assertEqual(expected, p.other_adventures)
         self.assertIsNot(g.adventures[p1], p.adventures)
         for a in p.adventures:
             self.assertIsNot(g.adventures[p1][a], p.adventures[a])

    def test_get_deck_remaining(self):
        p1 = 0
        g = gamestate.GameState()
        g.deck = list(deck.deck_gen())

        p = self.class_under_test(g, p1)

        self.assertEqual(len(g.deck), p.deck_remaining) 


