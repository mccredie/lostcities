

from . import gameproxybase

class PlayGameProxy(gameproxybase.GameProxyBase):
    def __init__(self, game, runner, player):
        super().__init__(game, player)
        self._runner = runner

    def play(self, index):
        self._game.play(self._player, index)
        self._runner.finish()

    def discard(self, index):
        self._game.discard(self._player, index)
        self._runner.finish()

