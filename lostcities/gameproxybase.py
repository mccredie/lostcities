
class GameProxyBase:
    def __init__(self, game, player):
        self._game = game
        self._player = player


    @property
    def hand(self):
        return self._game.hands[self._player][:]


    @property
    def discards(self):
        return frozenset(v[-1] 
                for v in self._game.discards.values()
                    if v)


    def _copy_adventures(self, player):
        adventures = {c:[] for c in 'rgbwy'}
        for c, v in self._game.adventures[player].items():
            adventures[c][:] = v
        return adventures


    @property
    def adventures(self):
        return self._copy_adventures(self._player)
                

    @property
    def other_adventures(self):
        return self._copy_adventures(self._player + 1 % 2)


    @property
    def deck_remaining(self):
        return len(self._game.deck)

