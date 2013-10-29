
from . import playgameproxy
from . import drawgameproxy


class GameRunnerState:
    def __init__(self, do, *args):
        self.next_state = self
        self._do = do
        self._args = args

    def update(self):
        self._do(*self._args)
        return self.next_state


def _get_init_state(p1, p2, runner, game):
    p1_play_proxy = playgameproxy.PlayGameProxy(game, runner, 0)
    p1_draw_proxy = drawgameproxy.DrawGameProxy(game, runner, 0)
    p2_play_proxy = playgameproxy.PlayGameProxy(game, runner, 1)
    p2_draw_proxy = drawgameproxy.DrawGameProxy(game, runner, 1)

    p1_play_card = GameRunnerState(p1.play_card, p1_play_proxy)
    p1_draw = GameRunnerState(p1.draw, p1_draw_proxy)
    p2_play_card = GameRunnerState(p2.play_card, p2_play_proxy)
    p2_draw = GameRunnerState(p2.draw, p2_draw_proxy)

    p1_play_card.next_state = p1_draw
    p1_draw.next_state = p2_play_card
    p2_play_card.next_state = p2_draw
    p2_draw.next_state = p1_play_card
    return p1_play_card


class GameRunner(object):
    def __init__(self, game, p1, p2):
        self._state = _get_init_state(p1, p2, self, game)
        self._game = game
        self.game_is_over = game.game_over

    def update(self):
        self._state = self._state.update()
        self.game_is_over = self._game.game_over

    def finish(self):
        pass


