
import random

SUITS = frozenset("rgbyw")
INVESTMENT = 'i'
VALUES = [INVESTMENT]*3 + list(range(2,11))

def deck_gen():
    for a in SUITS:
        for v in VALUES:
            yield a, v


