import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a text node",
                        TextType.BOLD, "http://fake.url.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq__different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_with_no_props(self):
        text_node = TextNode("text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual("b", html_node.tag)
        self.assertEqual("text", html_node.value)
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_with_props(self):
        text_node = TextNode("text", TextType.LINK, "link")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual("a", html_node.tag)
        self.assertEqual("text", html_node.value)
        self.assertEqual("link", html_node.props["href"])


if __name__ == "__main__":
    unittest.main()
