"""This file contains the test cases for text to HTML node function"""

import unittest

from text_to_html_node import text_node_to_html_node
from textnode import TextNode, TextType


class TestTextToHTMLNode(unittest.TestCase):
    """Class file containing the test cases for Text to HTML Node function"""

    def test_text(self):
        """Tests the conversion"""
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
