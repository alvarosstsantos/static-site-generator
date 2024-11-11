from __future__ import annotations

from typing import Dict, List


class HTMLNode():
    def __init__(self,
                 tag: str = None,
                 value: str = None,
                 children: List[HTMLNode] = None,
                 props: Dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        props_str = ""

        if self.props:
            for key, value in self.props.items():
                props_str = f'{props_str} {key}="{value}"'

        return props_str

    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children},"
                f" {self.props_to_html() if self.props else self.props})")
