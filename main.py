#!/usr/bin/env python
# encoding: utf-8


import random
import pprint
from collections import defaultdict

import lostcities



def init_game():
    game = lostcities.Game()
    game.deck[:] = lostcities.deck_gen()
    random.shuffle(game.deck)

    # deal
    for _ in range(7):
        for p in (0, 1):
            game.draw(p)

    return game


class CardValueGetter:
    def __init__(self, ivalue=None):
        if ivalue is None:
            ivalue = 11
        self._ivalue = ivalue
        
    def __call__(self, card):
        value = card[1]
        if value == lostcities.INVESTMENT:
            value = self._ivalue
        return value
        


class GameScorer:
    def __init__(self):
        self._adventures = defaultdict(lostcities.AdventureScorer);

    @staticmethod
    def from_dict(adventures):
        scorer = GameScorer()
        for stack in adventures.values():
            for value in stack:
                scorer.put(value)
        return scorer
    
    @staticmethod
    def from_gameproxy(game):
        return GameScorer.from_dict(game.adventures)

    
    @staticmethod
    def from_gamestate(game):
        return tuple(GameScorer.from_dict(game.players[p].adventures)
                for p in range(2))

        
    def put(self, card):
        suit, value = card
        self._adventures[suit].put(value)
        
    def score(self, suits=None):
        if suits is None:
            suits = self.active_suits
        total = 0
        for suit in suits:
            total += self._adventures[suit].score()
        return total
    
    def iter_scores(self):
        for k, v in self._adventures.items():
            yield k, v.score()
        
    @property
    def active_suits(self):
        return set(self._adventures)       

        

class TheOnePlayer(lostcities.Player):
    """ This player does the following:
        - Only begins playing on a stack when it knows it can achieve a score
          of 'risk'
        - Stops starting new piles when it is within 'cutoff' cards from the
          end of the deck.
        - Draws from draw piles that contain cards for adventures that it is
          involved in.
        - Discards cards that it cannot play
        - Discards lowest value card for inactive suits before active suits

    Note that this is still a heuristic AI.  It does not take into account
    what the other player is doing, or whether it may be benefiting the other
    player. 

    This is the first AI that I have implemented that is capable of fairly
    consistently beating the DiscardPlayer.  Although it isn't immensely
    complicated, it does illustrate how deceptively difficult this game is.
    """

    def __init__(self, risk=-5, cutoff=6):
        self._get_card_value = CardValueGetter()
        self._to_discard = []
        self._risk = risk
        self._cutoff = cutoff

        
    def _is_playable(self, card):
        stack = self._game.adventures[card[0]]
        if not stack:
            return True
        
        top_value = self._get_card_value(stack[-1])
        card_value = self._get_card_value(card)
        
        return top_value >= card_value  
        
        
    def _get_largest_playable(self, suits=None):
        if suits is None:
            suits = lostcities.SUITS
        
        for card in sorted(self._game.hand, reverse=True, 
                           key=self._get_card_value):
            if card[0] not in suits:
                continue
            if self._is_playable(card):
                return card
                
    
    def play_card(self, game):
        self._game = game
        scorer = GameScorer.from_gameproxy(game)
        active_suits = scorer.active_suits
        for suit in active_suits:
            score = scorer.score(suit)
            if score < 0:
                card = self._get_largest_playable(suit)
                if card is not None:
                    i = game.hand.index(card)
                    game.play(i)
                    return

        if game.deck_remaining > self._cutoff:
            suits_in_hand = set([card[0] for card in game.hand])        
            for card in sorted(game.hand, reverse=True, 
                               key=self._get_card_value):
                if self._is_playable(card):
                    scorer.put(card)
                else:
                    self._to_discard = []
    
            best_card = None
            best_score = self._risk       
            for suit in suits_in_hand:
                score = scorer.score(suit)
                if score > best_score:
                    best_card = self._get_largest_playable(suit)
                    best_score = score
            
            if best_card is not None:
                i = game.hand.index(best_card)            
                game.play(i)
                return
        
        if self._to_discard:
            for card in self._to_discard[:]:
                if card in game.hand:
                    i = game.hand.index(card)
                    game.discard(i)
                    self._to_discard.remove(card)
                    return
        

        inactive_suits = lostcities.SUITS - active_suits
        cards = sorted(game.hand, key=self._get_card_value)
        for card in cards:
            if card[0] in inactive_suits:
                game.discard(game.hand.index(card))
                return
        
        game.discard(game.hand.index(cards[0]))
            
    
    def draw(self, game):
        suits = set(s for s, c in game.adventures.items() if c)

        for card in game.discards:
            if card[0] in suits and self._is_playable(card):
                game.draw_from(card[0])
                return
        game.draw()


        
class GatedPlayer(lostcities.Player):
    def __init__(self, max_suits=2, ivalue=-11):
        self._get_value = CardValueGetter(ivalue)
        self._to_discard = []
        self._game = None
        self._suits_played = set()
        self._max_suits = max_suits
    
    def _find_last_played_card(self, suit):
        if self._game.adventures[suit]:
            return self._game.adventures[suit][-1]
    
    
    def _card_in_range(self, top, card):
        suit = card[0]
        if suit not in self._suits_played:
            if len(self._suits_played) >= self._max_suits:
                return False
            
        card_value = self._get_value(card)
        if top is None:
            return card_value >= 9          
        top_value = self._get_value(top)
        if card_value > top_value:
            self._to_discard.append(card)
        return top_value >= card_value > top_value - 4

    
    def _select_card(self, cards):
        for card in cards:
            last = self._find_last_played_card(card[0])
            if self._card_in_range(last, card):
                self._suits_played.add(card[0])
                return card

        
    def play_card(self, game):
        self._game = game        
        cards = sorted(self._game.hand, key=self._get_value, reverse=True)
        card_to_play = self._select_card(cards)

        
        if card_to_play is not None:
            i = game.hand.index(card_to_play)
            game.play(i)
        elif self._to_discard:
            for c in self._to_discard[:]:
                if c in game.hand:
                    game.discard(game.hand.index(c))
                    return
                else:
                    self._to_discard.remove(c)
        else:
            game.discard(game.hand.index(cards[-1]))
        

    def draw(self, game):
        for card in game.discards:
            if card[0] in self._suits_played:
                game.draw_from(card[0])
                break
        else:
            game.draw()


class RestrictedPlayer(lostcities.Player):
    def __init__(self, colors=lostcities.SUITS, minvalue=2, ivalue=None):
        self._colors = colors
        self._minvalue = minvalue
        self._get_value = CardValueGetter(ivalue)
        self._to_discard = []
        
    def play_card(self, game):
        cards = sorted(game.hand, key=self._get_value, reverse=True)
        for card in cards:
            if (card[0] in self._colors and 
                    self._get_value(card) >= self._minvalue):
                try:
                    i = game.hand.index(card)
                    game.play(i)

                except ValueError:
                    self._to_discard.append(card)
                else:
                    return
            else:
                self._to_discard.append(card)

        if self._to_discard:
            for c in self._to_discard[:]:
                if c in game.hand:
                    game.discard(game.hand.index(c))
                    return
                else:
                    self._to_discard.remove(c)
        else:
            game.discard(game.hand.index(cards[-1]))
        


    def draw(self, game):
        game.draw()


def can_play_on(top, card):
    if top is None or top == lostcities.INVESTMENT:
        return True
    if card == lostcities.INVESTMENT:
        return False
    return top > card


def get_remainder(card):
    """ Returns the list of card values that could possibly be played on top of
    the listed card.
    """
    v = card[1]
    if v == lostcities.INVESTMENT:
        v = 11
    return range(v-1, 1, -1)
    
    

class TrickyPlayer(lostcities.Player):
    def __init__(self):
        self.colors_played = set()
        self._to_discard = []
    
    def find_highest_possible_score(self):
        highest_score = -1000
        highest_index = None

        for i, card in enumerate(self._game.hand):
            scorer = lostcities.AdventureScorer()
            value = None
            for _, value in self._game.adventures[card[0]]:
                scorer.put(value)
            #start_score = scorer.score()
            if can_play_on(value, card[1]):
                for v in get_remainder(card):
                    scorer.put(v)
                increase = scorer.score() # - start_score
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
                except ValueError:
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


class DiscardPlayer(lostcities.Player):
    def play_card(self, game):
        game.discard(0)


    def draw(self, game):
        game.draw()


class StupidPlayer(lostcities.Player):
    def play_card(self, game):
        for i, card in enumerate(game.hand):
            try:
                game.play(i)
            except ValueError:
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
        scorer = lostcities.AdventureScorer()
        for suit, value in a:
            scorer.put(value)
        total += scorer.score()
    return total


def play_games(count, player=TrickyPlayer, *args, **kwargs):
    for _ in range(count):
        game = init_game()
        runner = lostcities.GameRunner(game, 
                player(*args, **kwargs), TheOnePlayer())

        while not runner.game_is_over:
            runner.update()

        yield GameScorer.from_dict(game.adventures[0]).score()


def main():
    game = init_game()
    runner = lostcities.GameRunner(game, TheOnePlayer(),
            TheOnePlayer())

    while not runner.game_is_over:
        runner.update()

    print("p1") 
    pprint.pprint(dict(game.players[0].adventures))
    print("total:", score(game.players[0].adventures))

    print("p2") 
    pprint.pprint(dict(game.players[1].adventures))
    print("total:", score(game.players[1].adventures))



if __name__ == "__main__":
    #main()

    from matplotlib.pyplot import hist
    from numpy import mean, std
    risk = -4
    cutoff = 8
    print("risk:", risk)
    print("cutoff:", cutoff)
    
    results = list(play_games(
            1000, TheOnePlayer, -4, 4))
            
    avg = mean(results)
    dev = std(results)
    print("mean:", avg)
    print("std dev:", dev)
    print("ratio:", avg / dev)
    hist(results)

    

