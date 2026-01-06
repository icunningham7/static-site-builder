from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(self):
    if self.text_type not in TextType:
        raise TypeError
    match self.text_type:
        case TextType.TEXT:
            return LeafNode(None, self.text)
        case TextType.BOLD:
            return LeafNode("b", self.text)
        case TextType.ITALIC:
            return LeafNode("i", self.text)
        case TextType.CODE:
            return LeafNode("code", self.text)
        case TextType.LINK:
            if self.url:
                return LeafNode("a", self.text, {"href": self.url})
            return LeafNode("a", self.text)
        case TextType.IMAGE:
            if self.url:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            return LeafNode("img", "", {"alt": self.text})
