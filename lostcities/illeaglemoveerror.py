
class IlleagleMoveError(Exception):
    """ Raised by *GameProxy classes when a player class attempts to perform
    more than one action on their turn. """
    pass
