
import random

ADVENTURES = "rgbyw"
VALUES = ['i']*3 + list(range(2,11))

def deck_gen():
    for a in ADVENTURES:
        for v in VALUES:
            yield a, v


