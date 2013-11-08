
from collections import defaultdict

from . import gamestate

class Game:
    def __init__(self, state=None):
        if state is None:
            state = gamestate.GameState()
        self.state = state


    @property
    def deck(self):
        return self.state.deck
    

    @property
    def discards(self):
        return self.state.discards

    @property
    def players(self):
        return self.state.players

    @property
    def game_over(self):
        return not bool(self.deck)


    def _check_player_value(self, player):
        if not 0 <= player <= 1: 
            raise ValueError("`player` must be 0 or 1", player)


    def draw(self, player):
        self._check_player_value(player)
        self.players[player].hand.append(self.deck.pop())


    def draw_from(self, player, adventure):
        self._check_player_value(player)
        the_card = self.discards[adventure].pop()
        self.players[player].hand.append(the_card)
        return the_card
        

    def _card_value(self, card):
        value = card[1]
        if value == 'i':
            value = 11
        return value


    def play(self, player, cardindex):
        self._check_player_value(player)
        card = self.players[player].hand[cardindex]
        adventure = card[0]
        adventure_pile = self.players[player].adventures[adventure]

        if (adventure_pile and 
                self._card_value(card) > self._card_value(adventure_pile[-1])):
            raise ValueError("Cannot play onto lower valued card.")

        del self.players[player].hand[cardindex]
        self.players[player].adventures[adventure].append(card)

        return card


    def discard(self, player, cardindex):
        self._check_player_value(player)
        card = self.players[player].hand.pop(cardindex)
        self.discards[card[0]].append(card)

        return card

