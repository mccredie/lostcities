
import unittest

from . import test_gameproxybase
from .. import playgameproxy


class StubGameState:
    def __init__(self):
        self.play_player = None
        self.play_card_index = None
        self.discard_player = None
        self.discard_card_index = None

    def play(self, player, card_index):
        self.play_player = player
        self.play_card_index = card_index

    def discard(self, player, card_index):
        self.discard_player = player
        self.discard_card_index = card_index

class StubGameRunner:
    def __init__(self):
        self.finish_called = False

    def finish(self):
        self.finish_called = True


class PlayGameProxyTests(test_gameproxybase.GameProxyBaseTests): 
    @staticmethod
    def class_under_test(g, p): 
        return playgameproxy.PlayGameProxy(g, None, p)


    def test_play_calls_play_with_same_card_index0(self):
        p0 = 0
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        index_to_play = 4

        p.play(index_to_play)

        self.assertEqual(index_to_play, g.play_card_index)


    def test_play_calls_play_with_same_index1(self):
        p0 = 0
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        index_to_play = 5

        p.play(index_to_play)

        self.assertEqual(index_to_play, g.play_card_index)


    def test_play_calls_play_with_same_player0(self):
        p0 = 0
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        p.play(4)

        self.assertEqual(p0, g.play_player)


    def test_play_calls_play_with_same_player1(self):
        p0 = 1
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        p.play(4)

        self.assertEqual(p0, g.play_player)

    def test_play_calls_finish_on_success(self):
        p0 = 1
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        p.play(4)

        self.assertTrue(r.finish_called)


    def test_discard_calls_discard_with_same_card_index0(self):
        p0 = 0
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        index_to_discard = 4

        p.discard(index_to_discard)

        self.assertEqual(index_to_discard, g.discard_card_index)


    def test_discard_calls_discard_with_same_index1(self):
        p0 = 0
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        index_to_discard = 5

        p.discard(index_to_discard)

        self.assertEqual(index_to_discard, g.discard_card_index)


    def test_discard_calls_discard_with_same_player0(self):
        p0 = 0
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        p.discard(4)

        self.assertEqual(p0, g.discard_player)


    def test_discard_calls_discard_with_same_player1(self):
        p0 = 1
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        p.discard(4)

        self.assertEqual(p0, g.discard_player)

    def test_discard_calls_finish_on_success(self):
        p0 = 1
        g = StubGameState()
        r = StubGameRunner()
        p = playgameproxy.PlayGameProxy(g, r, p0)

        p.discard(4)

        self.assertTrue(r.finish_called)


