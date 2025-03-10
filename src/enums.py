"""This file contains the enums used in this project"""

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


class BlockType(Enum):
    """Enum for managing block types

    Args:
        Enum (Enum): Base class Enum
    """

    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "q"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
