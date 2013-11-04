
import unittest

from .. import game
from .. import deck



class GameTests(unittest.TestCase):
    def test_draw_moves_top_card_from_deck_to_hand(self):
        player = 0
        g = game.Game()
        the_deck = list(deck.deck_gen())
        g.deck[:] = the_deck[:]

        g.draw(player) 

        self.assertEqual([the_deck[-1]], g.hands[player])
        self.assertEqual(the_deck[:-1], g.deck)

    
    def test_get_draw_from_moves_card_from_related_discard(self):
        player = 0
        adventure = 'r'
        g = game.Game()
        discards = [('r', 1), ('r', 2), ('r', 3) , ('r', 4)] 
        g.discards['r'][:] = discards[:]

        g.draw_from(player, 'r')

        self.assertEqual(g.discards['r'], discards[:-1])
        self.assertEqual(g.hands[player], [discards[-1]])


    def test_play_puts_card_in_adventure(self):
        player = 0
        g = game.Game()
        hand = [('r', 1), ('g', 2), ('b', 3) , ('b', 4)] 
        g.hands[player][:] = hand[:]

        g.play(player, 0)

        self.assertEqual([('r', 1)], g.adventures[player]['r'])
        self.assertEqual(hand[1:], g.hands[player])
    

    def test_discard_puts_card_in_correct_pile(self):
        player = 0
        g = game.Game()
        hand = [('r', 1), ('g', 2), ('b', 3) , ('b', 4)] 
        g.hands[player][:] = hand[:]

        g.discard(player, 1)

        self.assertEqual([('g', 2)], g.discards['g'])
        self.assertEqual([('r', 1), ('b', 3), ('b', 4)] , g.hands[player])


    def test_p2_draw_moves_top_card_from_deck_to_hand(self):
        player = 1
        g = game.Game()
        the_deck = list(deck.deck_gen())
        g.deck[:] = the_deck[:]

        g.draw(player) 

        self.assertEqual([the_deck[-1]], g.hands[player])
        self.assertEqual(the_deck[:-1], g.deck)

    
    def test_p2_get_draw_from_moves_card_from_related_discard(self):
        player = 1
        adventure = 'r'
        g = game.Game()
        discards = [('r', 1), ('r', 2), ('r', 3), ('r', 4)]  

        g.discards['r'] = discards[:]

        g.draw_from(player, 'r')

        self.assertEqual(g.discards['r'], discards[:-1])
        self.assertEqual([discards[-1]], g.hands[player])


    def test_p2_play_puts_card_in_adventure(self):
        player = 1
        g = game.Game()
        hand = [('r', 1), ('g', 2), ('b', 3) , ('b', 4)] 
        g.hands[player][:] = hand[:]

        g.play(player, 0)

        self.assertEqual([('r', 1)], g.adventures[player]['r'])
        self.assertEqual(hand[1:], g.hands[player])
    

    def test_p2_discard_puts_card_in_correct_pile(self):
        player = 1
        g = game.Game()
        hand = [('r', 1), ('g', 2), ('b', 3) , ('b', 4)] 
        g.hands[player][:] = hand[:]

        g.discard(player, 1)

        self.assertEqual([('g', 2)], g.discards['g'])
        self.assertEqual([('r', 1), ('b', 3), ('b', 4)] , g.hands[player])


    def test_gameover_set_on_last_draw(self):
        player = 0
        g = game.Game()
        g.deck[:] = [('r', 1)]

        g.draw(player)

        self.assertTrue(g.game_over)


    def test_play_raises_index_error_if_indexed_card_not_in_hand(self):
        player = 0
        g = game.Game()
        self.assertRaises(IndexError, g.play, player, 8)


    def test_discard_raises_index_error_if_indexed_card_not_in_hand(self):
        player = 0
        g = game.Game()
        self.assertRaises(IndexError, g.play, player, 8)


    def test_draw_raises_ValueError_on_bad_player_value(self):
        player = 40
        g = game.Game()
        self.assertRaises(ValueError, g.draw, player) 


    def test_draw_raises_TypeError_on_non_number_player_value(self):
        player = 'matt'
        g = game.Game()
        self.assertRaises(TypeError, g.draw, player) 


    def test_draw_from_raises_ValueError_on_bad_player_value(self):
        player = 40
        g = game.Game()
        self.assertRaises(ValueError, g.draw_from, player, 'r') 


    def test_draw_from_raises_TypeError_on_non_number_player_value(self):
        player = 'matt'
        g = game.Game()
        self.assertRaises(TypeError, g.draw_from, player, 'r') 


    def test_play_raises_ValueError_on_bad_player_value(self):
        player = 40
        g = game.Game()
        self.assertRaises(ValueError, g.play, player, 0) 


    def test_play_raises_TypeError_on_non_number_player_value(self):
        player = 'matt'
        g = game.Game()
        self.assertRaises(TypeError, g.play, player, 0) 


    def test_discard_raises_ValueError_on_bad_player_value(self):
        player = 40
        g = game.Game()
        self.assertRaises(ValueError, g.discard, player, 0) 


    def test_discard_raises_TypeError_on_non_number_player_value(self):
        player = 'matt'
        g = game.Game()
        self.assertRaises(TypeError, g.discard, player, 0) 


    def test_play_invest_on_number_raises_ValueError(self):
        player = 0
        g = game.Game()
        g.hands[player][:] = [('r', 'i')]
        g.adventures[player]['r'][:] = [('r', 2)]

        self.assertRaises(ValueError, g.play, player, 0)


    def test_play_invest_on_empty_succeeds(self):
        player = 0
        g = game.Game()
        g.hands[player][:] = [('r', 'i')]

        g.play(player, 0)

        self.assertEqual(('r', 'i'), g.adventures[player]['r'][0])


    def test_play_value_on_lower_value_raises_ValueError(self):
        player = 0
        g = game.Game()
        g.hands[player][:] = [('g', 5)]
        g.adventures[player]['g'][:] = [('g', 4)]

        self.assertRaises(ValueError, g.play, player, 0)


    def test_play_invest_on_invest_succeeds(self):
        player = 0
        g = game.Game()
        g.hands[player][:] = [('g', 'i')]
        g.adventures[player]['g'][:] = [('g', 'i')]

        g.play(player, 0)

        self.assertEqual([('g', 'i'), ('g', 'i')], g.adventures[player]['g'])


if __name__ == "__main__":
    unittest.main()

