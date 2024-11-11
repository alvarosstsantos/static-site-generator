import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode()
        self.assertIsNotNone(node)

    def test_empty_props_string(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

    def test_html_props_string(self):
        node = HTMLNode(None, None, [], {"prop1": "value1", "prop2": "value2"})
        self.assertEqual(' prop1="value1" prop2="value2"',
                         node.props_to_html())


if __name__ == "__main__":
    unittest.main()
