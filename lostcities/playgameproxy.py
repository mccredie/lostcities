

from . import gameproxybase
from .illeaglemoveerror import IlleagleMoveError

class PlayObserver:
    def finish_play(self):
        pass

    def finish_discard(self):
        pass


class PlayGameProxy(gameproxybase.GameProxyBase):
    def __init__(self, game, player, observer):
        super().__init__(game, player)
        self._observer = observer
        self._has_played = False

    def _ensure_legal_move(self):
        if self._has_played:
            raise IlleagleMoveError(
                    "Play action already performed.")

    def play(self, index):
        self._ensure_legal_move()
        card = self._game.play(self._player, index)
        self._observer.finish_play(card)
        self._has_played = True

    def discard(self, index):
        self._ensure_legal_move()
        card = self._game.discard(self._player, index)
        self._observer.finish_discard(card)
        self._has_played = True

