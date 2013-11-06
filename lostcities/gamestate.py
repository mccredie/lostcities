
from . import deck


class PlayerState:
    def __init__(self):
        self.hand = []
        self.adventures = {s: [] for s in deck.SUITS}


class GameState:
    def __init__(self):
        self.players = (PlayerState(), PlayerState())
        self.discards = {s: [] for s in deck.SUITS}
        self.deck = []




