from __future__ import annotations
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
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        delimeters = [i for i in range(
            len(old_node.text)) if old_node.text[i] == delimiter]

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
                    old_node.text[delimeters[i]:delimeters[i+1]+1],
                    text_type))
            else:
                new_nodes.append(
                    TextNode(old_node.text[delimeters[i]+1:delimeters[i+1]],
                             TextType.TEXT))

        if delimeters[-1] != len(old_node.text) - 1:
            new_nodes.append(
                TextNode(old_node.text[delimeters[-1]+1:],
                         TextType.TEXT))

    return new_nodes
