import helpers
import unittest
from models import Item


class HelperTestCase(unittest.TestCase):

    def setUp(self):
        self.glossary_base_url = "/projects/bailout/glossary/"

    def test_autogeneration_of_slug(self):
        item = self.create_troubled_asset()
        slug = item.slug
        self.assertEquals(slug, 'troubled-assets')

    def test_glossarize_with_1_glossary_item(self):
        self.create_warrant()
        plain = 'the warrants were issued'
        actual = helpers.glossarize(plain)
        expected = 'the <a href="%s#warrants">warrants</a> were issued' % self.glossary_base_url
        self.assertEquals(actual, expected)

    # def test_glossarize_with_2_glossary_items(self):

    def create_warrant(self):
        """This helper function creates a glossary item where the slug is
        already specified.
        """
        return self.create_item(
            "warrants",
            "warrants",
            """Options to buy stock (equity) at a specific price within a certain time frame. In this case, the specific terms will be agreed upon between Treasury and the respective bank."""
        )

    def create_troubled_asset(self):
        """This helper function creates a glossary items where the slug is
        not given.  So the model should automatically generate one.
        """
        return self.create_item(
            "troubled assets",
            "",
            """In relation to TARP, troubled assets are defined as any residential or commercial mortgages - or any stocks and bonds, debt or other instruments based on such mortgages - that originated or were issued on or before March 14, 2008, the purchase of which the Treasury Secretary determines promotes financial market stability. The term can also apply to any other financial instrument that the Secretary, after consulting with the Federal Reserve Chair, determines the purchase of which is necessary to promote financial market stability, but only after such determination is given in writing to appropriate Congressional committees."""
        )

    def create_item(self, term, slug, definition):
        item = Item()
        item.term = term
        if slug:
            item.slug = slug
        item.definition = definition
        item.save()
        return item

if __name__ == '__main__':
    unittest.main()
