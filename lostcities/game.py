
from collections import defaultdict

class Game:
    def __init__(self):
        self.hands = ([], [])
        self.adventures = (defaultdict(list), defaultdict(list))
        self.discards = defaultdict(list)
        self.game_over = False
        self.deck = []


    def _check_player_value(self, player):
        if not 0 <= player <= 1: 
            raise ValueError("`player` must be 0 or 1", player)


    def draw(self, player):
        self._check_player_value(player)
        self.hands[player].append(self.deck.pop())
        self.game_over = not self.deck


    def draw_from(self, player, adventure):
        self._check_player_value(player)
        self.hands[player].append(self.discards[adventure].pop())
        

    def _card_value(self, card):
        value = card[1]
        if value == 'i':
            value = 100
        return value


    def play(self, player, cardindex):
        self._check_player_value(player)
        card = self.hands[player][cardindex]
        adventure = card[0]
        adventure_pile = self.adventures[player][adventure]

        if (adventure_pile and 
                self._card_value(card) > self._card_value(adventure_pile[-1])):
            raise ValueError("Cannot play onto lower valued card.")

        del self.hands[player][cardindex]
        self.adventures[player][adventure].append(card)


    def discard(self, player, cardindex):
        self._check_player_value(player)
        card = self.hands[player].pop(cardindex)
        self.discards[card[0]].append(card)

