from __future__ import annotations

import re
from enum import Enum
from typing import List

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url,
                                        "alt": text_node.text})
        case _:
            raise TypeError()


def split_nodes_delimiter(old_nodes: List[TextNode],
                          delimiter: str,
                          text_type: TextType):
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

        if delimeters[-1] != len(old_node.text) - 1:
            new_nodes.append(
                TextNode(old_node.text[delimeters[-1]+step:],
                         TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]):
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


def split_nodes_link(old_nodes: List[TextNode]):
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


def text_to_textnodes(text):
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
