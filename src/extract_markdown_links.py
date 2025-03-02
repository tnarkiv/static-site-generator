"""This module contains code for extracting links from markdowns"""

import re


def extract_markdown_images(text: str):
    """This function extracts images from markdown text

    Args:
        text (str): Input markdown
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str):
    """This function extracts links from markdown text

    Args:
        text (str): Input markdown
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
