"""This file contains test cases for the split nodes delimiter functionality"""

import unittest

from split_node_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    """Class file containing test cases for split nodes delimiter"""

    def test_bold_text(self):
        """Tests whether bold text nodes are processed correctly"""
        node = TextNode("This is *bold* text", TextType.TEXT)
        node_list = [node]
        processed_node_list = split_nodes_delimiter(node_list, "*", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(processed_node_list, expected_nodes)


    def test_italic_text(self):
        """Tests whether italic text nodes are processed correctly"""
        node = TextNode("This is _italic_ text", TextType.TEXT)
        node_list = [node]
        processed_node_list = split_nodes_delimiter(node_list, "_", TextType.ITALICS)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALICS),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(processed_node_list, expected_nodes)


    def test_code_text(self):
        """Tests whether inline code text nodes are processed correctly"""
        node = TextNode("This is `code` text", TextType.TEXT)
        node_list = [node]
        processed_node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(processed_node_list, expected_nodes)


    def test_combined_bold_italic(self):
        """Tests bold and italic text in the same node"""
        node = TextNode("This is *bold* and _italic_ text", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "*", TextType.BOLD)
        processed_node_list = split_nodes_delimiter(node_list, "_", TextType.ITALICS)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALICS),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(processed_node_list, expected_nodes)


    def test_combined_bold_code(self):
        """Tests bold and code text in the same node"""
        node = TextNode("This is *bold* and `code` text", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "*", TextType.BOLD)
        processed_node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(processed_node_list, expected_nodes)
