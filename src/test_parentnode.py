"""This file contains test cases for Parent Nodes"""

import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    """This class file is used for testing Parent Node objects

    Args:
        unittest (TestCase): Base class TestCase
    """

    def test_eq(self):
        """This test creates two ParentNode objects with the same data
        and asserts that they are equal."""
        child_node = LeafNode("a", "website link", {"href": "https://www.google.com"})
        node = ParentNode("p", [child_node], {"class": "mx-3"})
        node2 = ParentNode("p", [child_node], {"class": "mx-3"})
        self.assertEqual(node, node2)

    def test_tag_not_eq(self):
        """This test creates two ParentNode objects with different tags and
        asserts that they are not equal"""
        node = ParentNode("h1", [])
        node2 = ParentNode("p", [])
        self.assertNotEqual(node, node2)

    def test_children_not_eq(self):
        """This test creates two ParentNode objects with different children and
        asserts that they are not equal"""
        child_node1 = LeafNode("p", "Random text")
        child_node2 = LeafNode("p", "Curated text")
        node = ParentNode("p", [child_node1], {})
        node2 = ParentNode("p", [child_node2], {})
        self.assertNotEqual(node, node2)

    def test_props_not_eq(self):
        """This test creates two ParentNode objects with different properties and
        asserts that they are not equal"""
        child_node = LeafNode("p", "Leaf text", {})
        node = LeafNode("a", [child_node], {"href": "https://www.google.com"})
        node2 = LeafNode("a", [child_node], {"href": "https://www.yahoo.com"})
        self.assertNotEqual(node, node2)

    def test_parent_to_html_p(self):
        """This test checks the to_html function of the parent nodes"""
        child_node1 = LeafNode("a", "Random text", {"href": "google"})
        child_node2 = LeafNode("a", "Curated text", {"href": "yahoo"})
        node = ParentNode("p", [child_node1, child_node2])
        self.assertEqual(
            node.to_html(),
            '<p><a href="google">Random text</a><a href="yahoo">Curated text</a></p>',
        )

    def test_to_html_with_grandchildren(self):
        """This test checks the to_html function of the parent node with nested children"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
