
import unittest

from . import drawgameproxy
from . import test_gameproxybase


class MockGameState:
    def __init__(self):
        self.draw_player = None
        self.draw_from_player = None
        self.draw_from_adventure = None

    def draw(self, player):
        self.draw_player = player

    def draw_from(self, player, adventure):
        self.draw_from_player = player
        self.draw_from_adventure = adventure

class StubGameRunner:
    def __init__(self):
        self.finish_called = False

    def finish(self):
        self.finish_called = True



class DrawGameProxyTests(test_gameproxybase.GameProxyBaseTests):
    @staticmethod
    def class_under_test(g, p): 
        return drawgameproxy.DrawGameProxy(g, None, p)

    def test_draw_calls_draw_with_player(self):
        p1 = 1
        g = MockGameState()
        r = StubGameRunner()
        p = drawgameproxy.DrawGameProxy(g, r, p1)
        p.draw()

        self.assertEqual(p1, g.draw_player)


    def test_draw_from_calls_draw_from_with_player(self):
        p1 = 1
        adventure = 'r'
        g = MockGameState()
        r = StubGameRunner()
        p = drawgameproxy.DrawGameProxy(g, r, p1)

        p.draw_from(adventure)

        self.assertEqual(p1, g.draw_from_player)
        self.assertEqual(adventure, g.draw_from_adventure)


    def test_draw_calls_finish_on_success(self):
        p1 = 1
        g = MockGameState()
        r = StubGameRunner()
        p = drawgameproxy.DrawGameProxy(g, r, p1)
        p.draw()

        self.assertTrue(r.finish_called)


    def test_draw_from_calls_finish_on_success(self):
        p1 = 1
        g = MockGameState()
        r = StubGameRunner()
        p = drawgameproxy.DrawGameProxy(g, r, p1)
        p.draw_from('r')

        self.assertTrue(r.finish_called)


