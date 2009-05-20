import unittest
import re
from utils.msub import msub_first
from utils.msub import msub_global
from utils.msub import _clean_match
from utils.no_self_wrapper import no_self_wrapper


class MsubFirstTestCase(unittest.TestCase):

    def test_independence_of_replacements(self):
        s = 'abcb'
        x = [('b', '<black>'), ('c', '<cat>'), ('a', '<air>')]
        r = msub_first(s, x)
        self.assertEqual(r, '<air><black><cat>b')


if __name__ == '__main__':
    unittest.main()
