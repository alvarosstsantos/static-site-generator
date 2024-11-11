import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = ParentNode("p", [LeafNode("b", "text")], None)
        self.assertIsNotNone(node)

    def test_error_to_html_no_tag(self):
        node = ParentNode(None, None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_error_to_html_no_children(self):
        node = ParentNode("p", None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_one_child(self):
        node = ParentNode("p", [LeafNode("b", "text")], None)
        self.assertEqual('<p><b>text</b></p>',
                         node.to_html())

    def test_to_html_mutilple_children(self):
        node = ParentNode("p",
                          [
                              LeafNode("b", "text"),
                              LeafNode("a", "text", {"prop": "value"})
                          ],
                          None)
        self.assertEqual('<p><b>text</b><a prop="value">text</a></p>',
                         node.to_html())

    def test_to_html_nested_parent(self):
        node = ParentNode("p",
                          [
                              ParentNode(
                                  "span", [LeafNode("b", "text")], None),
                              LeafNode("a", "text", {"prop": "value"})
                          ],
                          None)
        self.assertEqual(('<p><span><b>text</b></span>'
                          '<a prop="value">text</a></p>'),
                         node.to_html())


if __name__ == "__main__":
    unittest.main()
