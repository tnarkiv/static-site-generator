"""This module contains test cases for extracting markdown links"""

import unittest

from extract_markdown_links import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownLinks(unittest.TestCase):
    """Class file containing test cases for extracting markdown links"""

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
            "This is text with multiple images:  ![image_one](https://i.imgur.com/zjjcJKZ.png), \
                ![image_two](https://i.imgur.com/adfCVDe.png)"
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
            "This is text with the following links : [google](https://www.google.com),\
                  [yahoo](https://www.yahoo.com)"
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
