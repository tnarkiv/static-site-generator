"""This module contains the test cases for testing the utils class"""

import textwrap
import unittest

from textnode import TextNode
from enums import TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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
            TextNode(" in text", TextType.TEXT),
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
            TextNode(" out", TextType.TEXT),
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

    def setUp(self):
        self.text_types = TextType

    def test_plain_text_to_textnode(self):
        """Test conversion of plain text to textnode objects"""
        text = "Just plain text."
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, text)
        self.assertEqual(result[0].text_type, self.text_types.TEXT)

    def test_bold_text_to_textnode(self):
        """Test conversion of bold text to textnode objects"""
        text = "This is **bold** text."
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, self.text_types.BOLD)

    def test_italics_text_to_textnode(self):
        """Test conversion of italic text to textnode objects"""
        text = "This is _italic_ text."
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, self.text_types.ITALICS)

    def test_code_text_to_textnode(self):
        """Test conversion of code text to textnode objects"""
        text = "This is `code` text."
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, self.text_types.CODE)

    def test_mixed_formatting_to_textnode(self):
        """Test conversion of mixed text to textnode objects"""
        text = "**Bold** and _italic_ and `code`."
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0].text, "Bold")
        self.assertEqual(result[0].text_type, self.text_types.BOLD)
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[1].text_type, self.text_types.TEXT)
        self.assertEqual(result[2].text, "italic")
        self.assertEqual(result[2].text_type, self.text_types.ITALICS)
        self.assertEqual(result[3].text, " and ")
        self.assertEqual(result[3].text_type, self.text_types.TEXT)
        self.assertEqual(result[4].text, "code")
        self.assertEqual(result[4].text_type, self.text_types.CODE)
        self.assertEqual(result[5].text, ".")
        self.assertEqual(result[5].text_type, self.text_types.TEXT)

    def test_image_to_textnode(self):
        """Test conversion of images to textnode objects"""
        text = "This is an ![image](url)."
        result = text_to_textnodes(text)
        # Adjust this test based on how split_nodes_image works
        self.assertTrue(any(node.text_type == TextType.IMAGE for node in result))

    def test_link_to_textnode(self):
        """Test conversion of links to textnode objects"""
        text = "This is a [link](url)."
        result = text_to_textnodes(text)
        # Adjust this test based on how split_nodes_link works
        self.assertTrue(any(node.text_type == TextType.LINK for node in result))

    def test_single_paragraph_block(self):
        """Test that a single paragraph is correctly parsed into one block."""
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_multiple_paragraphs_block(self):
        """Test that multiple paragraphs are split into separate blocks."""
        md = textwrap.dedent(
            """
        This is the first paragraph.

        This is the second paragraph.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["This is the first paragraph.", "This is the second paragraph."]
        )

    def test_paragraph_with_line_breaks_block(self):
        """Test paragraphs with single newlines are treated as part of the same block."""
        md = textwrap.dedent(
            """
        This is the first line.
        This is still the same paragraph.

        Next paragraph starts here.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is the first line.\nThis is still the same paragraph.",
                "Next paragraph starts here.",
            ],
        )

    def test_leading_and_trailing_whitespace_block(self):
        """Test that leading and trailing whitespace is stripped."""
        md = textwrap.dedent(
            """
            
            This has leading and trailing whitespace.     

        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This has leading and trailing whitespace."])

    def test_list_items_block(self):
        """Test that lists are treated as single blocks."""
        md = textwrap.dedent(
            """
        - Item 1
        - Item 2

        - Item 3
        - Item 4
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2", "- Item 3\n- Item 4"])

    def test_code_blocks(self):
        """Test code blocks enclosed in triple backticks."""
        md = textwrap.dedent(
            """
        ```
        def hello():
            print("Hello, World!")
        ```

        Another paragraph.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                '```\ndef hello():\n    print("Hello, World!")\n```',
                "Another paragraph.",
            ],
        )

    def test_mixed_content(self):
        """Test paragraphs with bold, italics, code, and lists mixed together."""
        md = textwrap.dedent(
            """
        This is **bold** text.

        Here is _italic_ text and `code`.

        - List item 1
        - List item 2

        Another paragraph.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bold** text.",
                "Here is _italic_ text and `code`.",
                "- List item 1\n- List item 2",
                "Another paragraph.",
            ],
        )

    def test_consecutive_newlines(self):
        """Test paragraphs separated by more than two newlines."""
        md = textwrap.dedent(
            """
        Paragraph 1.


        Paragraph 2.

        Paragraph 3.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph 1.", "Paragraph 2.", "Paragraph 3."])

    def test_empty_input(self):
        """Test that empty input returns an empty list."""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        """Test that input with only whitespace returns an empty list."""
        md = "     \n    \n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_newline_within_paragraph(self):
        """Test single newlines within paragraphs are preserved."""
        md = textwrap.dedent(
            """
        This is line 1.
        This is line 2.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is line 1.\nThis is line 2."])

    def test_code_blocks_block(self):
        """Test code blocks enclosed in triple backticks."""
        md = textwrap.dedent(
            """
        ```
        def hello():
            print("Hello, World!")
        ```

        Another paragraph.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                '```\ndef hello():\n    print("Hello, World!")\n```',
                "Another paragraph.",
            ],
        )

    def test_mixed_content_block(self):
        """Test paragraphs with bold, italics, code, and lists mixed together."""
        md = textwrap.dedent(
            """
        This is **bold** text.

        Here is _italic_ text and `code`.

        - List item 1
        - List item 2

        Another paragraph.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bold** text.",
                "Here is _italic_ text and `code`.",
                "- List item 1\n- List item 2",
                "Another paragraph.",
            ],
        )

    def test_consecutive_newlines_block(self):
        """Test paragraphs separated by more than two newlines."""
        md = textwrap.dedent(
            """
        Paragraph 1.


        Paragraph 2.

        Paragraph 3.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph 1.", "Paragraph 2.", "Paragraph 3."])

    def test_empty_input_block(self):
        """Test that empty input returns an empty list."""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespace_block(self):
        """Test that input with only whitespace returns an empty list."""
        md = "     \n    \n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_newline_within_paragraph_block(self):
        """Test single newlines within paragraphs are preserved."""
        md = textwrap.dedent(
            """
        This is line 1.
        This is line 2.
        """
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is line 1.\nThis is line 2."])

    def test_paragraphs(self):
        """Tests markdown to html nodes with paragraphs
        """
        md = textwrap.dedent("""
            This is **bolded** paragraph text in a p tag here

            This is another paragraph with _italic_ text and `code` here

            """
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>"
            "This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        """Tests markdown to html node with code blocks
        """
        md = textwrap.dedent("""
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "</code></pre></div>",
        )

    def test_single_word_title(self):
        """Tests extract title with single word title
        """
        markdown = "# Title"
        self.assertEqual(extract_title(markdown), "Title")

    def test_multi_word_title(self):
        """Tests extract title with multi word title
        """
        markdown = "#  This is a Title "
        self.assertEqual(extract_title(markdown), "This is a Title")

    def test_title_with_extra_spaces(self):
        """Tests extract title with extra spaces
        """
        markdown = "#    Trimmed Title    "
        self.assertEqual(extract_title(markdown), "Trimmed Title")

    def test_no_h1_header(self):
        """Tests extract title with no H1 header
        """
        markdown = "## Not a Title\nSome text here"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found")

    def test_h1_among_other_headers(self):
        """Tests extract title with multiple headers
        """
        markdown = """
        ## Subtitle
        # Main Title
        ### Another Subtitle
        """
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_only_h1_with_no_text(self):
        """Tests extract title with empty header
        """
        markdown = "#  "
        self.assertEqual(extract_title(markdown), "")

    def test_h1_with_inline_markdown(self):
        """Tests extract title with header in inline markdown
        """
        markdown = "# **Bold Title**"
        self.assertEqual(extract_title(markdown), "**Bold Title**")

    def test_empty_input_extract_title(self):
        """Tests extract title with empty markdown
        """
        markdown = ""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found")
