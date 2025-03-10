"""This file contains the util functions used in the project"""

import re
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode
from enums import BlockType, TextType


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


def block_to_block_type(block: str):
    """
    Determines the type of a markdown block.

    Args:
        block (str): A single block of markdown text with leading and trailing whitespace removed.

    Returns:
        BlockType: The type of the markdown block.
    """
    lines = block.split("\n")

    if block.startswith("# ") or any(
        block.startswith(f"{'#' * i} ") for i in range(1, 7)
    ):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.lstrip().startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Converts a markdown string into an HTMLNode tree structure.

    Args:
        markdown (str): The markdown content to be converted.

    Returns:
        HTMLNode: The root node containing all block-level elements.
    """
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode(tag="div", children=[])

    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = None

        if block_type == BlockType.PARAGRAPH:
            block_node = ParentNode(tag="p", children=text_to_children(block))
        elif block_type == BlockType.HEADING:
            heading_level = min(block.count("#"), 6)
            block_node = ParentNode(
                tag=f"h{heading_level}", children=text_to_children(block.lstrip("# "))
            )
        elif block_type == BlockType.CODE:
            code_lines = block.splitlines()[1:-1]
            code_text = "\n".join(code_lines) + "\n"
            code_node = LeafNode(tag="code", value=code_text)
            block_node = ParentNode(tag="pre", children=[code_node])
        elif block_type == BlockType.QUOTE:
            quote_text = "\n".join(line.lstrip("> ") for line in block.splitlines())
            block_node = ParentNode(
                tag="blockquote", children=text_to_children(quote_text)
            )
        elif block_type == BlockType.UNORDERED_LIST:
            items = [line.lstrip("- ") for line in block.splitlines()]
            list_items = [
                ParentNode(tag="li", children=text_to_children(item)) for item in items
            ]
            block_node = ParentNode(tag="ul", children=list_items)
        elif block_type == BlockType.ORDERED_LIST:
            items = [line.split(". ", 1)[1] for line in block.splitlines()]
            list_items = [
                ParentNode(tag="li", children=text_to_children(item)) for item in items
            ]
            block_node = ParentNode(tag="ol", children=list_items)

        if block_node:
            parent_node.children.append(block_node)

    return parent_node


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Converts a text string into a list of HTMLNodes representing inline markdown.

    Args:
        text (str): The input text string with possible inline markdown.

    Returns:
        list[HTMLNode]: A list of HTMLNodes representing parsed inline elements.
    """
    nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        tag = None
        if node.text_type == TextType.BOLD:
            tag = "b"
        elif node.text_type == TextType.ITALICS:
            tag = "i"
        elif node.text_type == TextType.CODE:
            tag = "code"
        nodes.append(LeafNode(tag=tag, value=node.text))
    return nodes
