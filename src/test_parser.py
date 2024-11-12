import unittest
from parser import (BlockType, block_to_block_type, extract_markdown_images,
                    extract_markdown_links, markdown_to_blocks, markdown_to_html_node,
                    split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_children,
                    text_to_textnodes)

from textnode import TextNode, TextType


class TestParser(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = """
                # This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is the first list item in a list block
                * This is a list item
                * This is another list item
            """

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(3, len(blocks))

    def test_block_to_block_type_heading(self):
        block = "### titulo"

        res = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, res)

    def test_block_to_block_type_code(self):
        block = "```\ncodigo  \n```"

        res = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, res)

    def test_block_to_block_type_quote(self):
        block = "> ser ou nao ser eis a questao"

        res = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, res)

    def test_block_to_block_type_unordered_list(self):
        block = "* item 1\n* item 2"

        res = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, res)

    def test_block_to_block_type_ordered_list(self):
        block = "1. item 1\n2. item2"

        res = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, res)

    def test_block_to_block_type_paragraph(self):
        block1 = "```\ncodigo  "
        block2 = "*item 1\n- item 2"
        block3 = "1.item 1\n2. "
        block4 = "###"

        res1 = block_to_block_type(block1)
        self.assertEqual(BlockType.PARAGRAPH, res1)
        res2 = block_to_block_type(block2)
        self.assertEqual(BlockType.PARAGRAPH, res2)
        res3 = block_to_block_type(block3)
        self.assertEqual(BlockType.PARAGRAPH, res3)
        res4 = block_to_block_type(block4)
        self.assertEqual(BlockType.PARAGRAPH, res4)

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

    def test_text_to_children(self):
        text = ("This is **text** with an *italic* word and a "
                "`code block` and an ![obi wan image](https://i.imgur.com/"
                "fJRm4Vk.jpeg) and a [link](https://boot.dev)\n"
                "normal texto **vem**")

        children = text_to_children(text)

        self.assertEqual(1, len(children))
        self.assertEqual(12, len(children[0].children))

    def test_markdown_to_html_node(self):
        text = ("This is **text** with an *italic* word and a "
                "`code block` and an ![obi wan image](https://i.imgur.com/"
                "fJRm4Vk.jpeg) and a [link](https://boot.dev)\n"
                "normal texto **vem**")

        html_node = markdown_to_html_node(text)

        self.assertIsNotNone(html_node)
