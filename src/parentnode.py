from typing import Dict, List
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self,
                 tag: str,
                 children: List[HTMLNode],
                 props: Dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag argument required")

        if self.children is None or len(self.children) < 1:
            raise ValueError("Children argument required")

        children_str = ""

        for c in self.children:
            children_str += c.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"
