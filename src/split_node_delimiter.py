"""This file is used in converting Markdown to TextNodes"""

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
