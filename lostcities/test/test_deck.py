
from .. import deck
import unittest
import collections

class DeckTests(unittest.TestCase):
    def test_deck_has_correct_length(self):
        adventure_suits = 5 # r g b y w
        values = 9 # [2 - 10]
        investments = 3
        total_cards = (values + investments) * adventure_suits

        self.assertEqual(total_cards, len(list(deck.deck_gen())))

    def test_deck_contains_all_cards(self):
        """This is somewhat verbose and silly. Think of it as
           documentation. """

        # I'm using collections.Counter so that the order is ignored (as in a
        # set) but that multiples are accounted for.
        expected = collections.Counter([
                ('r', 'i'), ('r', 'i'), ('r', 'i'),
                ('r', 2), ('r', 3), ('r', 4), ('r', 5), ('r', 6), 
                ('r', 7), ('r', 8), ('r', 9), ('r', 10),

                ('g', 'i'), ('g', 'i'), ('g', 'i'),
                ('g', 2), ('g', 3), ('g', 4), ('g', 5), ('g', 6),
                ('g', 7), ('g', 8), ('g', 9), ('g', 10),

                ('b', 'i'), ('b', 'i'), ('b', 'i'),
                ('b', 2), ('b', 3), ('b', 4), ('b', 5), ('b', 6),
                ('b', 7), ('b', 8), ('b', 9), ('b', 10),

                ('y', 'i'), ('y', 'i'), ('y', 'i'),
                ('y', 2), ('y', 3), ('y', 4), ('y', 5), ('y', 6),
                ('y', 7), ('y', 8), ('y', 9), ('y', 10),

                ('w', 'i'), ('w', 'i'), ('w', 'i'),
                ('w', 2), ('w', 3), ('w', 4), ('w', 5), ('w', 6),
                ('w', 7), ('w', 8), ('w', 9), ('w', 10), ])

        self.assertEqual(expected, collections.Counter(deck.deck_gen()))



