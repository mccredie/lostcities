
import unittest

from .. import drawgameproxy
from .. import game
from . import test_gameproxybase


class MockGame:
    def __init__(self):
        self.draw_player = None
        self.draw_from_player = None
        self.draw_from_adventure = None
        self.draw_from_return = None

    def draw(self, player):
        self.draw_player = player

    def draw_from(self, player, adventure):
        self.draw_from_player = player
        self.draw_from_adventure = adventure
        return self.draw_from_return


class StubGameRunner:
    def __init__(self):
        self.finish_draw_called = False
        self.finish_draw_from_card = None

    def finish_draw(self):
        self.finish_draw_called = True

    def finish_draw_from(self, card):
        self.finish_draw_from_card = card


class DrawGameProxyTests(test_gameproxybase.GameProxyBaseTests):
    @staticmethod
    def class_under_test(g, p): 
        return drawgameproxy.DrawGameProxy(g, None, p)

    def test_draw_calls_draw_with_player(self):
        p1 = 1
        g = MockGame()
        r = StubGameRunner()
        p = drawgameproxy.DrawGameProxy(g, r, p1)
        p.draw()

        self.assertEqual(p1, g.draw_player)


    def test_draw_from_calls_draw_from_with_player(self):
        p1 = 1
        adventure = 'r'
        g = MockGame()
        r = StubGameRunner()
        p = drawgameproxy.DrawGameProxy(g, r, p1)

        p.draw_from(adventure)

        self.assertEqual(p1, g.draw_from_player)
        self.assertEqual(adventure, g.draw_from_adventure)


    def test_draw_calls_finish_on_success(self):
        p1 = 1
        g = MockGame()
        r = StubGameRunner()
        p = drawgameproxy.DrawGameProxy(g, r, p1)
        p.draw()

        self.assertTrue(r.finish_draw_called)


    def test_draw_from_calls_finish_with_correct_card(self):
        p1 = 1
        g = game.Game()
        card_to_draw = suit, _ = 'r', 10
        g.discards[suit].append(card_to_draw)

        r = StubGameRunner()
        p = drawgameproxy.DrawGameProxy(g, r, p1)

        p.draw_from(suit)

        self.assertEqual(card_to_draw, r.finish_draw_from_card)
        
