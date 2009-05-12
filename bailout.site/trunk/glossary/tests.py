import helpers
import unittest

class HelperTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def testSomething(self):
        s = 'Get ready to hear a lot about TARP'
        expected = 'Get ready to hear a lot about <a href="/glossary#tarp">TARP</a>'
        actual = helpers.glossarize(s)
        self.assertEquals(actual, expected)

if __name__ == '__main__':
    unittest.main()
