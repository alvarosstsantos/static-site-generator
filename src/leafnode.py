from typing import Dict
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self,
                 tag: str,
                 value: str,
                 props: Dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()

        if self.tag:
            return (f"<{self.tag}{self.props_to_html()}>"
                    f"{self.value}</{self.tag}>")
        else:
            return self.value
