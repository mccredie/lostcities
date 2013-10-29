import unittest

from .. import adventure


class AdventureTests(unittest.TestCase):
    def test_score_0_cards__0(self):
        a = adventure.Adventure()
        self.assertEqual(0, a.score())


    def test_score_one_invest_only__neg40(self):
        a = adventure.Adventure()
        a.put('i')
        self.assertEqual(-40, a.score())


    def test_score_two_invest_only__neg60(self):
        a = adventure.Adventure()
        a.put('i')
        a.put('i')
        self.assertEqual(-60, a.score())


    def test_score_two_invest_only__neg80(self):
        a = adventure.Adventure()
        a.put('i')
        a.put('i')
        a.put('i')
        self.assertEqual(-80, a.score())


    def test_score_max__136(self):
        a = adventure.Adventure()
        a.put('i')
        a.put('i')
        a.put('i')
        a.put(10)
        a.put(9)
        a.put(8)
        a.put(7)
        a.put(6)
        a.put(5)
        a.put(4)
        a.put(3)
        a.put(2)
        self.assertEqual(136, a.score())

    def test_typical__20(self):
        a = adventure.Adventure()
        a.put('i')
        a.put(9)
        a.put(7)
        a.put(6)
        a.put(5)
        a.put(3)
        self.assertEqual(20, a.score())


    def test_typical_bad__neg5(self):
        a = adventure.Adventure()
        a.put(7)
        a.put(5)
        a.put(3)
        self.assertEqual(-5, a.score())



if __name__ == "__main__":
    unittest.main()
