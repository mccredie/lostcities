
import unittest

from .. import gamerunner
from .. import playgameproxy
from .. import drawgameproxy


class PlayerStub:
    def __init__(self):
        self.play_card_called = False
        self.draw_called = False
        self.play_proxy = None
        self.draw_proxy = None


    def play_card(self, play_proxy):
        self.play_card_called = True
        self.play_proxy = play_proxy


    def draw(self, draw_proxy):
        self.draw_called = True
        self.draw_proxy = draw_proxy


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


    def test_second_update_passes_drawproxy_to_p1_draw(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)
        runner.update()
        runner.update()

        self.assertIsInstance(p1.draw_proxy, drawgameproxy.DrawGameProxy)



    def test_update_call_p1_draw(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)
        runner.update()
        self.assertFalse(p1.draw_called)
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
        runner.update()
        self.assertTrue(p1.play_card_called)
        self.assertTrue(p1.draw_called)


    def test_update_calls_p2_play_card_on_second_turn(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)

        runner.update()
        runner.update()
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
        runner.update()
        runner.update()
        self.assertFalse(p2.draw_called)
        runner.update()
        self.assertTrue(p2.draw_called)


    def test_update_calls_p1_play_card_on_third_turn(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)

        runner.update()
        runner.update()
        runner.update()
        runner.update()
        p1.play_card_called = False
        runner.update()

        self.assertTrue(p1.play_card_called)

    def test_update_calls_p1_draw_on_third_turn(self):
        p1 = PlayerStub()
        p2 = PlayerStub()
        state = GameStateStub()
        runner = gamerunner.GameRunner(state, p1, p2)

        runner.update()
        runner.update()
        runner.update()
        runner.update()
        runner.update()
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
        



if __name__ == "__main__":
    unittest.main()

