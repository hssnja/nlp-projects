"""Small regression suite; run with python -m unittest -v."""

import unittest

from next_word import NGramPredictor
from tokenizer import tokenize


class TokenizerTests(unittest.TestCase):
    def test_empty_and_whitespace(self):
        self.assertEqual(tokenize(" \n\t"), [])

    def test_letters_numbers_and_punctuation(self):
        self.assertEqual(tokenize("Hello123, WORLD!"),
                         ["hello", "123", ",", "world", "!"])

    def test_persian(self):
        self.assertEqual(tokenize("سلام، دنیا."), ["سلام", "،", "دنیا", "."])
        self.assertEqual(tokenize("سلام، دنیا.", prediction_mode=True),
                         ["سلام", "دنیا"])

    def test_original_project_difference(self):
        self.assertEqual(tokenize(".5"), [".", "5"])
        self.assertEqual(tokenize(".5", prediction_mode=True), [".5"])


class PredictorTests(unittest.TestCase):
    def setUp(self):
        self.model = NGramPredictor("i like green tea i like green tea i like black coffee")

    def test_all_orders(self):
        for order, text, expected in [(1, "", "i"), (2, "i", "like"),
                                      (3, "i like", "green"),
                                      (4, "i like green", "tea")]:
            with self.subTest(order=order):
                self.assertEqual(self.model.predict(text, order), expected)

    def test_tie_uses_first_seen(self):
        self.assertEqual(NGramPredictor("a z a b").predict("a", 2), "z")

    def test_unseen_context(self):
        self.assertIsNone(self.model.predict("unknown", 2))

    def test_short_corpus(self):
        model = NGramPredictor("hello")
        self.assertEqual(model.predict("", 1), "hello")
        self.assertIsNone(model.predict("hello", 2))

    def test_invalid_inputs(self):
        for order in [0, 5, -1, 1.5, True]:
            with self.subTest(order=order), self.assertRaises(ValueError):
                self.model.predict("i like green", order)
        with self.assertRaises(ValueError):
            self.model.predict("i", 3)
        for corpus in ["", " \n", ". ،"]:
            with self.subTest(corpus=corpus), self.assertRaises(ValueError):
                NGramPredictor(corpus)

    def test_instances_are_independent(self):
        other = NGramPredictor("i run")
        self.assertEqual(other.predict("i", 2), "run")
        self.assertEqual(self.model.predict("i", 2), "like")


if __name__ == "__main__":
    unittest.main()
