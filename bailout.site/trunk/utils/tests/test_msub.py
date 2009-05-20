import unittest
import re
from utils.msub import msub_first
from utils.msub import msub_global
from utils.msub import _clean_match
from utils.no_self_wrapper import no_self_wrapper


class SharedExamples():

    def test_interwoven_matches_1(self):
        """
        Same setup as test_interwoven_matches_2 but the order of the
        transformation list is reversed.

        Abbreviations:
        * s is short for 'string'
        * x is short for 'xform' or 'transform'
        * r is short for result
        """
        s = 'the Loan Guarantee was'
        x = [('loan guarantee', '<*>'), ('loan', '<*>')]
        r = self.function_to_test(s, x)
        self.assertEqual(r, 'the <Loan Guarantee> was')

    def test_interwoven_matches_2(self):
        """
        Same setup as test_interwoven_matches_1 but the order of the
        transformation list is reversed.
        """
        s = 'the Loan Guarantee was'
        x = [('loan', '<*>'), ('loan guarantee', '<*>')]
        r = self.function_to_test(s, x)
        self.assertEqual(r, 'the <Loan> Guarantee was')

    def test_capitalization_is_preserved(self):
        s = 'Equity considerations mean that'
        x = [('equity', '<*>')]
        r = self.function_to_test(s, x)
        self.assertEqual(r, '<Equity> considerations mean that')

class MsubGlobalTestCase(unittest.TestCase, SharedExamples):
    function_to_test = no_self_wrapper(msub_global)

    def test_independence_of_replacements(self):
        s = 'abcb'
        x = [('b', '<black>'), ('c', '<cat>'), ('a', '<air>')]
        r = msub_global(s, x)
        self.assertEqual(r, '<air><black><cat><black>')


class MsubFirstTestCase(unittest.TestCase, SharedExamples):
    function_to_test = no_self_wrapper(msub_first)

    def test_independence_of_replacements(self):
        s = 'abcb'
        x = [('b', '<black>'), ('c', '<cat>'), ('a', '<air>')]
        r = msub_first(s, x)
        self.assertEqual(r, '<air><black><cat>b')

    def test_link_to_csv(self):
        "Text inside of tags should be off-limits"
        s = 'more <a href="/media/1.csv">data</a> that'
        x = [('csv', '<*>'), ('media', '<*>')]
        r = msub_first(s, x)
        self.assertEqual(r, 'more <a href="/media/1.csv">data</a> that')

    def test_two_replacements(self):
        "Text inside of tags should be off-limits"
        s = """TARP allows the United States Department of the Treasury to purchase or insure up to $700 billion of "troubled" assets.  See this <a href="/data/2009.csv">link</a> for more information."""
        x = [
            ('treasury', '<a href="/glossary/#treasury">*</a>'),
            ('csv',      '<a href="/glossary/#csv">*</a>')]
        r = msub_first(s, x)
        self.assertEqual(r, """TARP allows the United States Department of the <a href="/glossary/#treasury">Treasury</a> to purchase or insure up to $700 billion of "troubled" assets.  See this <a href="/data/2009.csv">link</a> for more information.""")


class CleanMatchTest(unittest.TestCase):
    
    def test_simple(self):
        m = re.search('me', '---me---')
        list = [
            ([],       True),
            ([(0, 1)], True),
            ([(1, 2)], True),
            ([(2, 3)], True),
            ([(3, 4)], False),
            ([(4, 5)], False),
            ([(5, 6)], True),
            ([(6, 7)], True),
            ([(7, 8)], True),
            ([(0, 2)], True),
            ([(1, 3)], True),
            ([(2, 4)], False),
            ([(3, 5)], False),
            ([(4, 6)], False),
            ([(5, 7)], True),
            ([(6, 8)], True)]
        for spans, expected in list:
            result = _clean_match(m, spans)
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
