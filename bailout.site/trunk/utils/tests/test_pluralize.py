import unittest
from utils.pluralize import pluralize

class PluralizeTestCase(unittest.TestCase):

    def test_s_endings(self):
        self.assertPlurals([
            ('dog',           'dogs'),
            ('finance',       'finances'),
            ('human',         'humans'),
            ('instrument',    'instruments'),
            ('loan',          'loans'),
            ('Transaction',   'Transactions')
        ])

    def test_es_endings(self):
        self.assertPlurals([
            ('box',           'boxes')
        ])

    def test_ies_endings(self):
        self.assertPlurals([
            ('Secretary',     'Secretaries'),
            ('dairy',         'dairies'),
            ('Debt Security', 'Debt Securities')
        ])

    def test_irregulars(self):
        self.assertPlurals([
            ('knife',         'knives'),
            ('life',          'lives'),
            ('ox',            'oxen'),
            ('person',        'people'),
            ('woman',         'women')
        ])

    def test_unchanging_nouns(self):
        self.assertPlurals([
            ('data',          'data'),
            ('fish',          'fish')
        ])

    def assertPlurals(self, pairs):
        for pair in pairs:
            self.assertEqual(pluralize(pair[0]), pair[1])

if __name__ == '__main__':
    unittest.main()
