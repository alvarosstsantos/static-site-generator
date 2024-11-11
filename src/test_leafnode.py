import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode(None, "text", None)
        self.assertIsNotNone(node)

    def test_no_tag(self):
        node = LeafNode(None, "text", None)
        self.assertEqual("text", node.to_html())

    def test_tag(self):
        node = LeafNode("p", "text", None)
        self.assertEqual("<p>text</p>", node.to_html())

    def test_html_props_string(self):
        node = LeafNode("b", "text", {"prop": "value"})
        self.assertEqual('<b prop="value">text</b>',
                         node.to_html())


if __name__ == "__main__":
    unittest.main()
