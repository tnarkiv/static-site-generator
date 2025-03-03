"""This module contains the test cases for testing the utils class"""

import unittest

from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class TestUtils(unittest.TestCase):
    """This is the class file containing the test cases for the Utils file"""

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

    def test_extract_markdown_images_no_image(self):
        """Test the extract markdown images function with no image"""
        matches = extract_markdown_images("This is text with no image.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_one_image(self):
        """Tests the extract markdown images function with one image"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple_image(self):
        """Tests the extract markdown images function with multiple images"""
        matches = extract_markdown_images(
            "This is text with multiple images:  ![image_one](https://i.imgur.com/zjjcJKZ.png), "
            "![image_two](https://i.imgur.com/adfCVDe.png)"
        )
        self.assertListEqual(
            [
                ("image_one", "https://i.imgur.com/zjjcJKZ.png"),
                ("image_two", "https://i.imgur.com/adfCVDe.png"),
            ],
            matches,
        )

    def test_extract_markdown_links_no_link(self):
        """Tests the extract markdown links function with no link"""
        matches = extract_markdown_links("This is text with no link.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_one_link(self):
        """Test the extract markdown links function with one link"""
        matches = extract_markdown_links(
            "This is text with one link [google](https://www.google.com)"
        )
        self.assertListEqual(([("google", "https://www.google.com")]), matches)

    def test_extract_markdown_links_multiple_links(self):
        """Test the extract markdown links function with multiple link"""
        matches = extract_markdown_links(
            "This is text with the following links : [google](https://www.google.com),"
            "[yahoo](https://www.yahoo.com)"
        )
        self.assertListEqual(
            (
                [
                    ("google", "https://www.google.com"),
                    ("yahoo", "https://www.yahoo.com"),
                ]
            ),
            matches,
        )

    def test_split_nodes_image(self):
        """This test case checks the split nodes images function with multiple images"""
        node_one = TextNode("![alt text](image_url)", TextType.TEXT)
        node_two = TextNode("This is ![an image](url) in text", TextType.TEXT)
        node_list = [node_one, node_two]

        processed_nodes = split_nodes_image(node_list)
        expected_nodes = [
            TextNode("alt text", TextType.IMAGE, "image_url"),
            TextNode("This is ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "url"),
            TextNode(" in text", TextType.TEXT)
        ]
        self.assertEqual(processed_nodes, expected_nodes)

    def test_split_nodes_link(self):
        """This test case checks the split nodes link function with multiple links"""
        node_one = TextNode("[link text](link_url)", TextType.TEXT)
        node_two = TextNode("Check this [example](url) out", TextType.TEXT)
        node_list = [node_one, node_two]

        processed_nodes = split_nodes_link(node_list)
        expected_nodes = [
            TextNode("link text", TextType.LINK, "link_url"),
            TextNode("Check this ", TextType.TEXT),
            TextNode("example", TextType.LINK, "url"),
            TextNode(" out", TextType.TEXT)
        ]
        self.assertEqual(processed_nodes, expected_nodes)

    def test_no_images_or_links(self):
        """This test case checks the split nodes and images link 
        functions with no images or links"""
        node = TextNode("Just plain text", TextType.TEXT)
        node_list = [node]

        processed_images = split_nodes_image(node_list)
        processed_links = split_nodes_link(node_list)

        self.assertEqual(processed_images, node_list)
        self.assertEqual(processed_links, node_list)
