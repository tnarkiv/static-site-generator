"""Contains code for rendering text nodes"""

from enum import Enum


class TextType(Enum):
    """Enum for managing text types

    Args:
        Enum (Enum): base class Enum
    """

    TEXT = "text"
    BOLD = "bold"
    ITALICS = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """Text node class"""

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node_two):
        """Checks for equivalence of two text nodes

        Args:
            node_two (TextNode): Second Node
        """
        if (
            self.text == node_two.text
            and self.text_type == node_two.text_type
            and self.url == node_two.url
        ):
            return True
        else:
            return False

    def __repr__(self):
        """Returns a string representation of the text node"""
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
