"""This file contains the util functions used in the project"""

import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    """Splits text nodes using multi-character delimiters like '**'."""
    new_node_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) == 1:
            new_node_list.append(node)
            continue

        if len(parts) % 2 == 0:
            raise ValueError(
                f'Invalid markdown syntax: Unmatched opening delimiter "{delimiter}"'
            )

        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_node_list.append(TextNode(part, TextType.TEXT))
            else:
                new_node_list.append(TextNode(part, text_type))

    return new_node_list


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


def split_nodes_image(old_nodes: list[TextNode]):
    """Splits text nodes containing images

    Args:
        old_nodes (list[TextNode]): List of text nodes to be processed

    Returns:
        list[TextNodes]: List of processed nodes split on found images
    """
    new_node_list: list[TextNode] = []
    pattern = re.compile(r"(!\[([^\[\]]*)\]\(([^\(\)]*)\))")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
            continue

        last_index = 0
        for match in pattern.finditer(node.text):
            start, end = match.span()
            alt_text, image_url = match.group(2), match.group(3)

            if start > last_index:
                new_node_list.append(
                    TextNode(node.text[last_index:start], TextType.TEXT)
                )

            new_node_list.append(TextNode(alt_text, TextType.IMAGE, image_url))
            last_index = end

        if last_index < len(node.text):
            new_node_list.append(TextNode(node.text[last_index:], TextType.TEXT))

    return new_node_list


def split_nodes_link(old_nodes: list[TextNode]):
    """Splits text nodes containing links

    Args:
        old_nodes (list[TextNode]): List of text nodes to be processed

    Returns:
        list[TextNodes]: List of processed nodes split on found links
    """
    new_node_list: list[TextNode] = []
    pattern = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
            continue

        last_index = 0
        for match in pattern.finditer(node.text):
            start, end = match.span()
            link_text, link_url = match.group(1), match.group(2)

            if start > last_index:
                new_node_list.append(
                    TextNode(node.text[last_index:start], TextType.TEXT)
                )

            new_node_list.append(TextNode(link_text, TextType.LINK, link_url))
            last_index = end

        if last_index < len(node.text):
            new_node_list.append(TextNode(node.text[last_index:], TextType.TEXT))

    return new_node_list


def text_to_textnodes(text: str):
    """Converts a raw string of markdown-flavored text into a list of TextNode objects

    Args:
        text (str): Markdown text

    Returns:
        List(TextNode): Textnodes created from Markdown text
    """
    nodes_list = [TextNode(text, TextType.TEXT)]
    delimiters = [("**", TextType.BOLD), ("_", TextType.ITALICS), ("`", TextType.CODE)]

    for delimiter, text_type in delimiters:
        nodes_list = split_nodes_delimiter(nodes_list, delimiter, text_type)

    for split_func in [split_nodes_image, split_nodes_link]:
        nodes_list = split_func(nodes_list)
    return nodes_list


def markdown_to_blocks(text: str):
    """Converts a markdown string to list of block strings

    Args:
        text (str): Input Markdown string

    Returns:
        list(str): list of block strings
    """
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    return blocks
