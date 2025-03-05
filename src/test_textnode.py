"""This file contains test cases for text nodes"""

import unittest

from textnode import TextNode
from enums import TextType


class TestTextNode(unittest.TestCase):
    """Class TestTextNode

    Args:
        unittest (unittest.TestCase): base class TestCase
    """

    def test_eq(self):
        """This test creates two TextNode objects with the same properties 
        and asserts that they are equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        """This test creates two TextNode objects with different texts and
        asserts that they are not equal."""
        node = TextNode("Random text", TextType.ITALICS)
        node2 = TextNode("Not Random text", TextType.ITALICS)
        self.assertNotEqual(node, node2)

    def test_text_type_not_eq(self):
        """This test creates two TextNode objects with different text types and
        asserts that they are not equal."""
        node = TextNode("Random text", TextType.BOLD)
        node2 = TextNode("Not Random text", TextType.ITALICS)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        """This test creates two TextNode objects with different texts and
        asserts that they are not equal."""
        node = TextNode("Random text", TextType.ITALICS, "https://www.google.com")
        node2 = TextNode("Not Random text", TextType.ITALICS, "https://www.yahoo.co.in")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
