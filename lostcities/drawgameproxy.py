

from .gameproxybase import GameProxyBase
from .illeaglemoveerror import IlleagleMoveError


class DrawObserver:
    def finish_draw(self):
        pass

    def finish_draw_from(self):
        pass


class DrawGameProxy(GameProxyBase):
    def __init__(self, game, player, observer):
        super().__init__(game, player)
        self._observer = observer
        self._draw_complete = False

    def _ensure_legal(self):
        if self._draw_complete:
            raise IlleagleMoveError(
                    "Player cannot perform two draw actions in the same turn.")


    def draw(self):
        self._ensure_legal()
        self._game.draw(self._player)
        self._observer.finish_draw()
        self._draw_complete = True


    def draw_from(self, adventure):
        self._ensure_legal()
        card = self._game.draw_from(self._player, adventure)
        self._observer.finish_draw_from(card)
        self._draw_complete = True

