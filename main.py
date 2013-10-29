
import random
import pprint

import lostcities

def init_game():
    game = lostcities.GameState()
    thedeck = list(lostcities.deck_gen())

    random.shuffle(thedeck)
    game.deck = thedeck

    # deal
    for _ in range(7):
        for p in (0, 1):
            game.draw(p)

    return game


class RestrictedPlayer(object):
    def play_card(self, game):
        for i, card in enumerate(game.hand):
            if card[0] in 'rgb':
                try:
                    game.play(i)
                except ValueError as e:
                    pass
                else:
                    break
        else:
            game.discard(0)


    def draw(self, game):
        game.draw()

def can_play_on(top, card):
    if top is None or top == 'i':
        return True
    if card == 'i':
        return False
    return top > card


def get_remainder(card):
    v = card[1]
    if v == 'i':
        v = 11
    return range(v-1, 1, -1)

class LargestPlayer(object):
    def __init__(self, m=0.5, b=20):
        self.m = m
        self.b = b
        self.colors_played = set()
        self._to_discard = []
    
    def find_highest_possible_score(self):
        highest_score = -1000
        highest_index = None

        for i, card in enumerate(self._game.hand):
            scorer = lostcities.Adventure()
            value = None
            for _, value in self._game.adventures[card[0]]:
                scorer.put(value)
            start_score = scorer.score()
            if can_play_on(value, card[1]):
                for v in get_remainder(card):
                    scorer.put(v)
                increase = scorer.score() - start_score 
                if increase > highest_score:
                    highest_score = increase
                    highest_index = i
            else:
                self._to_discard.append(card)
            if highest_score > 0:
                return highest_index
    

    def play_card(self, game):
        self._game = game
        i = self.find_highest_possible_score()
        if i is None:
            if self._to_discard:
                try:
                    index = game.hand.index(self._to_discard.pop())
                except ValueError as e:
                    game.discard(0)
                else:
                    game.discard(index)
            else:
                game.discard(0)
        else:
            game.play(i)


    def draw(self, game):
        self._game = game
        game.draw()


class DiscardPlayer(object):
    def play_card(self, game):
        game.discard(0)


    def draw(self, game):
        game.draw()


class StupidPlayer(object):
    def play_card(self, game):
        for i, card in enumerate(game.hand):
            try:
                game.play(i)
            except ValueError as e:
                pass
            else:
                break
        else:
            game.discard(0)


    def draw(self, game):
        game.draw()


def score(adventures):
    total = 0
    for a in adventures.values():
        scorer = lostcities.Adventure()
        for suit, value in a:
            scorer.put(value)
        total += scorer.score()
    return total


def main():
    game = init_game()
    runner = lostcities.GameRunner(game, LargestPlayer(0.25, 0),
            LargestPlayer(0.75, 40))

    while not runner.game_is_over:
        runner.update()

    print("p1") 
    pprint.pprint(dict(game.adventures[0]))
    print("total:", score(game.adventures[0]))

    print("p2") 
    pprint.pprint(dict(game.adventures[1]))
    print("total:", score(game.adventures[1]))


if __name__ == "__main__":
    main()

