"""This file contains the test cases for leafnode.py (Leaf Nodes)"""

import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    """This class file is used for testing Leaf Node objects

    Args:
        unittest (TestCase): Base class TestCase
    """

    def test_eq(self):
        """This test creates two HTMLNode objects with the same data
        and asserts that they are equal."""
        node = LeafNode("a", "Test paragraph", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Test paragraph", {"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_tag_not_eq(self):
        """This test creates two LeafNode objects with different tags and
        asserts that they are not equal"""
        node = LeafNode("a", "")
        node2 = LeafNode("p", "")
        self.assertNotEqual(node, node2)

    def test_value_not_eq(self):
        """This test creates two LeafNode objects with different tags and
        asserts that they are not equal"""
        node = LeafNode("p", "Random text")
        node2 = LeafNode("p", "Curated text")
        self.assertNotEqual(node, node2)

    def test_props_not_eq(self):
        """This test creates two LeafNode objects with different properties and
        asserts that they are not equal"""
        node = LeafNode("p", "Random text", {"href": "https://www.google.com"})
        node2 = LeafNode("p", "Curated text", {"href": "https://www.yahoo.com"})
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        """This test checks the to_html function of the leaf nodes"""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
