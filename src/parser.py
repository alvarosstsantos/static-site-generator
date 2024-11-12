
import re
from enum import Enum
from typing import List

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paraghraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes: List[TextNode],
                          delimiter: str,
                          text_type: TextType) -> List[TextNode]:
    step = len(delimiter)
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        delimeters = []
        i = 0

        while True:
            try:
                i = old_node.text.index(delimiter, i)
                delimeters.append(i)

                i += step
            except ValueError:
                break

        if len(delimeters) == 0:
            new_nodes.append(old_node)
            continue

        if len(delimeters) % 2 != 0:
            raise Exception("Invalid Markdown syntax")

        new_nodes.append(
            TextNode(old_node.text[:delimeters[0]], TextType.TEXT))

        for i in range(len(delimeters) - 1):
            if i % 2 == 0:
                new_nodes.append(TextNode(
                    old_node.text[delimeters[i]:delimeters[i+1]+step],
                    text_type))
            else:
                new_nodes.append(
                    TextNode(old_node.text[delimeters[i]+step:delimeters[i+1]],
                             TextType.TEXT))

        if delimeters[-1] + step != len(old_node.text):
            new_nodes.append(
                TextNode(old_node.text[delimeters[-1]+step:],
                         TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        split_text = ["", old_node.text]

        for image_alt, image_link in images:
            split_text = split_text[1].split(
                f"![{image_alt}]({image_link})", 1)

            if (len(split_text) > 0 and split_text[0] != ""):
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

        if len(split_text) > 1 and split_text[1] != "":
            new_nodes.append(TextNode(split_text[1], TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        split_text = ["", old_node.text]

        for link_text, link_url in links:
            split_text = split_text[1].split(
                f"[{link_text}]({link_url})", 1)

            if (len(split_text) > 0 and split_text[0] != ""):
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

        if len(split_text) > 1 and split_text[1] != "":
            new_nodes.append(TextNode(split_text[1], TextType.TEXT))

    return new_nodes


def text_to_textnodes(text) -> List[TextNode]:
    bold_nodes = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(
        bold_nodes, "*", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(
        italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)

    return split_nodes_link(image_nodes)


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def markdown_to_blocks(markdown: str) -> List[str]:
    return (list(
        filter(lambda block: block,
               map(lambda block: block.strip(), markdown.split("\n\n")))))


def block_to_block_type(block: str):
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if re.match(r"^```[\S\s]+```$", block):
        return BlockType.CODE
    if re.match(r"^>", block):
        return BlockType.QUOTE
    if re.match(r"^[\*-]\s", block):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\.\s", block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    content = list(map(block_to_html_node, markdown_to_blocks(markdown)))

    return ParentNode("html", [ParentNode("body", content)])


def block_to_html_node(block: str) -> ParentNode:
    match(block_to_block_type(block)):
        case BlockType.PARAGRAPH:
            return block_to_paragraph_node(block)
        case BlockType.HEADING:
            return block_to_heading_node(block)
        case BlockType.CODE:
            return block_to_code_node(block)
        case BlockType.QUOTE:
            return block_to_quote_node(block)
        case BlockType.UNORDERED_LIST:
            return block_to_unordered_list_node(block)
        case BlockType.ORDERED_LIST:
            return block_to_ordered_list_node(block)
        case _:
            raise TypeError()


def block_to_unordered_list_node(block: str):
    list_items = list(
        map(lambda i: ParentNode("li", text_to_children(i)),
            map(lambda line: line[2:], block.split("\n"))))

    return ParentNode("ul", list_items)


def block_to_ordered_list_node(block: str):
    list_items = list(
        map(lambda i: ParentNode("li", text_to_children(i)),
            map(lambda line: line[line.index(".") + 2:], block.split("\n"))))

    return ParentNode("ol", list_items)


def block_to_paragraph_node(block: str):
    return ParentNode("p", text_to_children(block))


def block_to_quote_node(block: str):
    quote = "\n".join(map(lambda line: line[1:], block.split("\n")))
    return ParentNode("blockquote", text_to_children(quote))


def block_to_heading_node(block: str):
    level = 0

    for c in block:
        if c != "#":
            break

        level += 1

    return ParentNode(f"h{level}", text_to_children(block[level+1:]))


def block_to_code_node(block: str):
    code_node = ParentNode("code", text_to_children(block[3:-3]))
    return ParentNode("pre", [code_node])


def text_to_children(text: str) -> List[LeafNode]:
    text_nodes = []

    for line in map(text_to_textnodes, text.split("\n")):
        text_nodes.extend(line)

    return [ParentNode("div", [text_node_to_html_node(n) for n in text_nodes])]
