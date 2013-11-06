
import copy

class GameProxyBase:
    def __init__(self, game, player):
        self._game = game
        self._player = player


    @property
    def hand(self):
        return self._game.players[self._player].hand[:]


    @property
    def discards(self):
        return frozenset(v[-1] 
                for v in self._game.discards.values()
                    if v)

    @property
    def adventures(self):
        return copy.deepcopy(self._game.players[self._player].adventures)
                

    @property
    def other_adventures(self):
        other_player = (self._player + 1) % 2
        return copy.deepcopy(self._game.players[other_player].adventures)


    @property
    def deck_remaining(self):
        return len(self._game.deck)

