import unittest
from utils.msub import msub_first
from utils.msub import msub_global
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
        s = 'more <a href="/media/1.csv">data</a> that'
        x = [('csv', '<*>'), ('media', '<*>')]
        r = msub_first(s, x)
        self.assertEqual(r, 'more <a href="/media/1.csv">data</a> that')

if __name__ == '__main__':
    unittest.main()
