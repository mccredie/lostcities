
import unittest

from .. import game
from .. import deck
from .. import gamestate



class GameTests(unittest.TestCase):
    def test_draw_moves_top_card_from_deck_to_hand(self):
        p = 0
        g = game.Game()
        the_deck = list(deck.deck_gen())
        g.deck[:] = the_deck[:]

        g.draw(p)

        self.assertEqual([the_deck[-1]], g.players[p].hand)
        self.assertEqual(the_deck[:-1], g.deck)


    def test_get_draw_from_moves_card_from_related_discard(self):
        p = 0
        adventure = 'r'
        g = game.Game()
        discards = [('r', 1), ('r', 2), ('r', 3) , ('r', 4)]
        g.discards['r'][:] = discards[:]

        g.draw_from(p, 'r')

        self.assertEqual(g.discards['r'], discards[:-1])
        self.assertEqual(g.players[p].hand, [discards[-1]])

    def test_get_draw_from_returns_the_drawn_card(self):
        p = 0
        adventure = 'r'
        g = game.Game()
        top_card = ('r', 4)
        discards = [('r', 1), ('r', 2), ('r', 3) , top_card]
        g.discards['r'][:] = discards[:]

        self.assertEqual(top_card, g.draw_from(p, 'r'))

        self.assertEqual(g.discards['r'], discards[:-1])
        self.assertEqual(g.players[p].hand, [discards[-1]])


    def test_play_puts_card_in_adventure(self):
        p = 0
        g = game.Game()
        hand = [('r', 1), ('g', 2), ('b', 3) , ('b', 4)]
        g.players[p].hand[:] = hand[:]

        g.play(p, 0)

        self.assertEqual([('r', 1)], g.players[p].adventures['r'])
        self.assertEqual(hand[1:], g.players[p].hand)


    def test_play_returns_played_card(self):
        p = 0
        g = game.Game()
        the_card = ('r', 1)
        hand = [the_card, ('g', 2), ('b', 3) , ('b', 4)]
        g.players[p].hand[:] = hand[:]

        self.assertEqual(the_card, g.play(p, 0))


    def test_discard_puts_card_in_correct_pile(self):
        p = 0
        g = game.Game()
        hand = [('r', 1), ('g', 2), ('b', 3) , ('b', 4)]
        g.players[p].hand[:] = hand[:]

        g.discard(p, 1)

        self.assertEqual([('g', 2)], g.discards['g'])
        self.assertEqual([('r', 1), ('b', 3), ('b', 4)] , g.players[p].hand)


    def test_discard_returns_discarded_card(self):
        p = 0
        g = game.Game()
        the_card = ('g', 2)
        hand = [('r', 1), the_card, ('b', 3) , ('b', 4)]
        g.players[p].hand[:] = hand[:]

        self.assertEqual(the_card, g.discard(p, 1))


    def test_p2_draw_moves_top_card_from_deck_to_hand(self):
        p = 1
        g = game.Game()
        the_deck = list(deck.deck_gen())
        g.deck[:] = the_deck[:]

        g.draw(p)

        self.assertEqual([the_deck[-1]], g.players[p].hand)
        self.assertEqual(the_deck[:-1], g.deck)


    def test_p2_get_draw_from_moves_card_from_related_discard(self):
        p = 1
        adventure = 'r'
        g = game.Game()
        discards = [('r', 1), ('r', 2), ('r', 3), ('r', 4)]

        g.discards['r'] = discards[:]

        g.draw_from(p, 'r')

        self.assertEqual(g.discards['r'], discards[:-1])
        self.assertEqual([discards[-1]], g.players[p].hand)


    def test_p2_play_puts_card_in_adventure(self):
        p = 1
        g = game.Game()
        hand = [('r', 1), ('g', 2), ('b', 3) , ('b', 4)]
        g.players[p].hand[:] = hand

        g.play(p, 0)

        self.assertEqual([('r', 1)], g.players[p].adventures['r'])
        self.assertEqual(hand[1:], g.players[p].hand)


    def test_p2_discard_puts_card_in_correct_pile(self):
        p = 1
        g = game.Game()
        hand = [('r', 1), ('g', 2), ('b', 3) , ('b', 4)]
        g.players[p].hand[:] = hand

        g.discard(p, 1)

        self.assertEqual([('g', 2)], g.discards['g'])
        self.assertEqual([('r', 1), ('b', 3), ('b', 4)] , g.players[p].hand)


    def test_gameover_set_on_last_draw(self):
        p = 0
        g = game.Game()
        g.deck[:] = [('r', 1)]

        g.draw(p)

        self.assertTrue(g.game_over)


    def test_play_raises_index_error_if_indexed_card_not_in_hand(self):
        p = 0
        g = game.Game()
        self.assertRaises(IndexError, g.play, p, 8)


    def test_discard_raises_index_error_if_indexed_card_not_in_hand(self):
        p = 0
        g = game.Game()
        self.assertRaises(IndexError, g.play, p, 8)


    def test_draw_raises_ValueError_on_bad_player_value(self):
        p = 40
        g = game.Game()
        self.assertRaises(ValueError, g.draw, p)


    def test_draw_raises_TypeError_on_non_number_player_value(self):
        p = 'matt'
        g = game.Game()
        self.assertRaises(TypeError, g.draw, p)


    def test_draw_from_raises_ValueError_on_bad_player_value(self):
        p = 40
        g = game.Game()
        self.assertRaises(ValueError, g.draw_from, p, 'r')


    def test_draw_from_raises_TypeError_on_non_number_player_value(self):
        p = 'matt'
        g = game.Game()
        self.assertRaises(TypeError, g.draw_from, p, 'r')


    def test_play_raises_ValueError_on_bad_player_value(self):
        p = 40
        g = game.Game()
        self.assertRaises(ValueError, g.play, p, 0)


    def test_play_raises_TypeError_on_non_number_player_value(self):
        p = 'matt'
        g = game.Game()
        self.assertRaises(TypeError, g.play, p, 0)


    def test_discard_raises_ValueError_on_bad_player_value(self):
        p = 40
        g = game.Game()
        self.assertRaises(ValueError, g.discard, p, 0)


    def test_discard_raises_TypeError_on_non_number_player_value(self):
        p = 'matt'
        g = game.Game()
        self.assertRaises(TypeError, g.discard, p, 0)


    def test_play_invest_on_number_raises_ValueError(self):
        p = 0
        g = game.Game()
        g.players[p].hand[:] = [('r', 'i')]
        g.players[p].adventures['r'][:] = [('r', 2)]

        self.assertRaises(ValueError, g.play, p, 0)


    def test_play_invest_on_empty_succeeds(self):
        p = 0
        g = game.Game()
        g.players[p].hand[:] = [('r', 'i')]

        g.play(p, 0)

        self.assertEqual(('r', 'i'), g.players[p].adventures['r'][0])


    def test_play_value_on_higher_value_raises_ValueError(self):
        p = 0
        g = game.Game()
        g.players[p].hand[:] = [('g', 4)]
        g.players[p].adventures['g'][:] = [('g', 5)]

        self.assertRaises(ValueError, g.play, p, 0)


    def test_play_invest_on_invest_succeeds(self):
        p = 0
        g = game.Game()
        g.players[p].hand[:] = [('g', 'i')]
        g.players[p].adventures['g'][:] = [('g', 'i')]

        g.play(p, 0)

        self.assertEqual([('g', 'i'), ('g', 'i')],
                g.players[p].adventures['g'])


    def test_players_returns_state_players(self):
        state = gamestate.GameState()
        g = game.Game(state)

        self.assertIs(state.players, g.players)


    def test_discards_returns_state_discards(self):
        state = gamestate.GameState()
        g = game.Game(state)

        self.assertIs(state.discards, g.discards)


    def test_deck_returns_state_deck(self):
        state = gamestate.GameState()
        g = game.Game(state)

        self.assertIs(state.deck, g.deck)



if __name__ == "__main__":
    unittest.main()

