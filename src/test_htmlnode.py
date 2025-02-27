"""This file contains test cases for HTML Node"""

import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    """This class file is used for testing HTML Node objects

    Args:
        unittest (TestCase): Base class TestCase
    """

    def test_eq(self):
        """This test creates two HTMLNode objects with the same properties
        and asserts that they are equal."""
        child_node = HTMLNode()
        node = HTMLNode(
            "p", "Test paragraph", [child_node], {"href": "https://www.google.com"}
        )
        node2 = HTMLNode(
            "p", "Test paragraph", [child_node], {"href": "https://www.google.com"}
        )
        self.assertEqual(node, node2)

    def test_tag_not_eq(self):
        """This test creates two HTMLNode objects with different tags and
        asserts that they are not equal"""
        node = HTMLNode("a")
        node2 = HTMLNode("p")
        self.assertNotEqual(node, node2)

    def test_value_not_eq(self):
        """This test creates two HTMLNode objects with different tags and
        asserts that they are not equal"""
        node = HTMLNode("p", "Random text")
        node2 = HTMLNode("p", "Curated text")
        self.assertNotEqual(node, node2)

    def test_children_not_eq(self):
        """This test creates two HTMLNode objects with different tags and
        asserts that they are not equal"""
        child_node = HTMLNode()
        node = HTMLNode("p", "Random text", [child_node])
        node2 = HTMLNode("p", "Curated text")
        self.assertNotEqual(node, node2)

    def test_props_not_eq(self):
        """This test creates two HTMLNode objects with different tags and
        asserts that they are not equal"""
        child_node = HTMLNode()
        node = HTMLNode(
            "p", "Random text", [child_node], {"href": "https://www.google.com"}
        )
        node2 = HTMLNode(
            "p", "Curated text", [child_node], {"href": "https://www.yahoo.com"}
        )
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        """This test checks the props_to_html function"""
        node = HTMLNode(
            None, None, None, {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )
