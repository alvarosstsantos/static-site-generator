import unittest

from textnode import (TextNode, TextType, extract_markdown_images,
                      extract_markdown_links, split_nodes_delimiter,
                      split_nodes_image, split_nodes_link,
                      text_node_to_html_node, text_to_textnodes)


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

    def test_split_nodes_delimiter(self):
        node1 = TextNode(
            "This is text with a `code block 1` word`code block 2`",
            TextType.TEXT)
        node2 = TextNode("**bold block**", TextType.BOLD)

        new_nodes1 = split_nodes_delimiter([node1, node2], "`", TextType.CODE)

        self.assertEqual(5, len(new_nodes1))
        self.assertEqual("This is text with a ", new_nodes1[0].text)
        self.assertEqual("`code block 1`", new_nodes1[1].text)
        self.assertEqual(" word", new_nodes1[2].text)
        self.assertEqual("`code block 2`", new_nodes1[3].text)
        self.assertEqual("**bold block**", new_nodes1[4].text)

        new_nodes2 = split_nodes_delimiter(new_nodes1, "**", TextType.BOLD)

        self.assertEqual(5, len(new_nodes2))

    def test_extract_markdown_images(self):
        text = ("This is text with a ![rick roll](https://i.imgur.com/aK.gif)"
                " and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")

        res = extract_markdown_images(text)

        self.assertEqual([("rick roll", "https://i.imgur.com/aK.gif"),
                         ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], res)

    def test_extract_markdown_links(self):
        text = ("This is text with a link [to boot dev](https://www.boot.dev)"
                " and [to youtube](https://www.youtube.com/@boot)")

        res = extract_markdown_links(text)

        self.assertEqual([("to boot dev", "https://www.boot.dev"),
                         ("to youtube", "https://www.youtube.com/@boot")], res)

    def test_split_nodes_links(self):
        node = TextNode(
            ("This is text with a link [to boot dev](https://www.boot.dev)"
             " and [to youtube](https: // www.youtube.com/@bootdotdev)"),
            TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertEqual(4, len(new_nodes))
        self.assertEqual("This is text with a link ", new_nodes[0].text)
        self.assertEqual("to boot dev", new_nodes[1].text)
        self.assertEqual(" and ", new_nodes[2].text)
        self.assertEqual("to youtube", new_nodes[3].text)

    def test_split_nodes_image(self):
        node = TextNode(
            ("This is text with a link ![to boot dev](https://www.boot.dev)"
             " and ![to youtube](https: // www.youtube.com/@bootdotdev)"),
            TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertEqual(4, len(new_nodes))
        self.assertEqual("This is text with a link ", new_nodes[0].text)
        self.assertEqual("to boot dev", new_nodes[1].text)
        self.assertEqual(" and ", new_nodes[2].text)
        self.assertEqual("to youtube", new_nodes[3].text)

    def test_text_to_textnodes(self):
        text = ("This is **text** with an *italic* word and a "
                "`code block` and an ![obi wan image](https://i.imgur.com/"
                "fJRm4Vk.jpeg) and a [link](https://boot.dev)")

        nodes = text_to_textnodes(text)

        self.assertEqual(10, len(nodes))


if __name__ == "__main__":
    unittest.main()
