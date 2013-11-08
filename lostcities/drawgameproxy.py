
from .gameproxybase import GameProxyBase

class DrawGameProxy(GameProxyBase):
    def __init__(self, game, runner, player):
        super().__init__(game, player)
        self._runner = runner


    def draw(self):
        self._game.draw(self._player)
        self._runner.finish_draw()


    def draw_from(self, adventure):
        card = self._game.draw_from(self._player, adventure)
        self._runner.finish_draw_from(card)

