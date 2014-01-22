
import unittest

from .. import gamerunner
from .. import playgameproxy
from .. import drawgameproxy



class PlayerStub(gamerunner.Player):
    def __init__(self):
        self.play_card_called = False
        self.draw_called = False
        self.play_proxy = None
        self.draw_proxy = None
        self.they_discarded_card = None
        self.they_played_card = None
        self.they_drew_called = False
        self.they_drew_from_card = None


    def play_card(self, play_proxy):
        self.play_card_called = True
        self.play_proxy = play_proxy


    def draw(self, draw_proxy):
        self.draw_called = True
        self.draw_proxy = draw_proxy


    def they_discarded(self, card):
        self.they_discarded_card = card


    def they_played(self, card):
        self.they_played_card = card


    def they_drew(self):
        self.they_drew_called = True


    def they_drew_from(self, card):
        self.they_drew_from_card = card



class RaisingPlayerStub(gamerunner.Player):
    def __init__(self):
        self.play_card_raise = None
        self.draw_raise = None


    def play_card(self, play_proxy):
        if self.play_card_raise is not None:
            raise self.play_card_raise


    def draw(self, draw_proxy):
        if self.draw_raise is not None:
            raise self.play_card_raise




class GameStateStub:
    def __init__(self):
        self.game_over = False



class GameRunnerTests(unittest.TestCase):
    def test_update_call_p1_play_card(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)
        runner.update()

        self.assertTrue(p1.play_card_called)


    def test_update_passes_playproxy_to_p1_play_card(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)
        runner.update()

        self.assertIsInstance(p1.play_proxy, playgameproxy.PlayGameProxy)


    def test_second_update_without_finish_calls_p1_play_again(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()

        self.assertIsInstance(p1.draw_proxy, drawgameproxy.DrawGameProxy)


    def test_second_update_passes_drawproxy_to_p1_draw(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)
        runner.update()
        # clear the call
        p1.play_card_called = False
        runner.update()
        # it gets called again because the previous call didn't finish
        self.assertTrue(p1.play_card_called)


    def test_update_call_p1_draw(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)
        runner.update()
        self.assertFalse(p1.draw_called)
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()
        self.assertTrue(p1.draw_called)


    def test_update_call_play_card_then_draw(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)

        self.assertFalse(p1.play_card_called)
        self.assertFalse(p1.draw_called)
        runner.update()
        self.assertTrue(p1.play_card_called)
        self.assertFalse(p1.draw_called)
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()
        self.assertTrue(p1.play_card_called)
        self.assertTrue(p1.draw_called)


    def test_update_calls_p2_play_card_on_second_turn(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)

        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_draw()
        self.assertFalse(p2.play_card_called)
        self.assertFalse(p2.draw_called)
        runner.update()
        self.assertTrue(p2.play_card_called)


    def test_update_calls_p2_draw_on_second_turn(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)

        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_discard(None)
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        self.assertFalse(p2.draw_called)
        runner.update()
        self.assertTrue(p2.draw_called)


    def test_update_calls_p1_play_card_on_third_turn(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)

        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_draw()
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_draw()
        p1.play_card_called = False
        runner.update()

        self.assertTrue(p1.play_card_called)


    def test_update_calls_p1_draw_on_third_turn(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)

        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_draw()
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_draw()
        runner.update()
        # simulating finish callback - this should come from the proxy
        runner.finish_play(None)
        p1.draw_called = False
        runner.update()

        self.assertTrue(p1.draw_called)


    def test_report_game_over(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        state.game_over = True

        runner = gamerunner.GameRunner(state, p1, p2)

        self.assertTrue(runner.game_is_over)


    def test_report_game_not_over(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()

        runner = gamerunner.GameRunner(state, p1, p2)
        self.assertFalse(runner.game_is_over)
        

    def test_p2_passed_p1_played_card(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        the_card = 'w', 4

        runner = gamerunner.GameRunner(state, p1, p2)
        
        runner.update()

        self.assertIsNone(p2.they_played_card)
        runner.finish_play(the_card)
        self.assertEqual(the_card, p2.they_played_card)


    def test_p2_passed_p1_discarded_card(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        the_card = 'w', 4

        runner = gamerunner.GameRunner(state, p1, p2)
        
        runner.update()

        self.assertIsNone(p2.they_discarded_card)
        runner.finish_discard(the_card)
        self.assertEqual(the_card, p2.they_discarded_card)


    def test_they_drew_called_on_p2(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()

        runner = gamerunner.GameRunner(state, p1, p2)
        
        runner.update()
        runner.finish_play(None)
        runner.update()

        self.assertFalse(p2.they_drew_called)
        runner.finish_draw()
        self.assertTrue(p2.they_drew_called)


    def test_p2_passed_p1_they_drew_from_card(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        the_card = 'g', 7

        runner = gamerunner.GameRunner(state, p1, p2)
        
        runner.update()
        runner.finish_play(None)
        runner.update()

        self.assertIsNone(p2.they_drew_from_card)
        runner.finish_draw_from(the_card)
        self.assertTrue(the_card, p2.they_drew_from_card)


    def test_p1_passed_p2_played_card(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        the_card = 'w', 4

        runner = gamerunner.GameRunner(state, p1, p2)
        
        runner.update()
        runner.finish_play(None)
        runner.update()
        runner.finish_draw()
        runner.update()

        self.assertIsNone(p1.they_played_card)
        runner.finish_play(the_card)
        self.assertEqual(the_card, p1.they_played_card)


    def test_p1_passed_p2_discarded_card(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        the_card = 'w', 4

        runner = gamerunner.GameRunner(state, p1, p2)
        
        runner.update()
        runner.finish_play(None)
        runner.update()
        runner.finish_draw()
        runner.update()

        self.assertIsNone(p1.they_discarded_card)
        runner.finish_discard(the_card)
        self.assertEqual(the_card, p1.they_discarded_card)


    def test_they_drew_called_on_p1(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()

        runner = gamerunner.GameRunner(state, p1, p2)
        
        runner.update()
        runner.finish_play(None)
        runner.update()
        runner.finish_draw()
        runner.update()
        runner.finish_play(None)
        runner.update()

        self.assertFalse(p1.they_drew_called)
        runner.finish_draw()
        self.assertTrue(p1.they_drew_called)


    def test_p1_passed_p2_they_drew_from_card(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        the_card = 'g', 7

        runner = gamerunner.GameRunner(state, p1, p2)
        
        runner.update()
        runner.finish_play(None)
        runner.update()
        runner.finish_draw()
        runner.update()
        runner.finish_play(None)
        runner.update()

        self.assertIsNone(p1.they_drew_from_card)
        runner.finish_draw_from(the_card)
        self.assertTrue(the_card, p1.they_drew_from_card)


        







