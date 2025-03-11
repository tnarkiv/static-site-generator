"""This module generates a web page from markdown file"""

import os

from utils import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str):
    """
    Generates an HTML page from a markdown file and template.

    Args:
        from_path (str): Path to the source markdown file.
        template_path (str): Path to the HTML template file.
        dest_path (str): Path to the destination HTML file.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    final_content = template_content.replace("{{ Title }}", title)
    final_content = final_content.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(final_content)

    print(f"Page generated at {dest_path}")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    """
    Recursively generates HTML pages from markdown files.

    Args:
        dir_path_content (str): Path to the content directory containing markdown files.
        template_path (str): Path to the HTML template file.
        dest_dir_path (str): Path to the destination directory for generated HTML files.
    """
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(
                    dest_dir_path, os.path.splitext(relative_path)[0] + ".html"
                )

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(from_path, template_path, dest_path)
                print(f"Generated page: {dest_path}")
