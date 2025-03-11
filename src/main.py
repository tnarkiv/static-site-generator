"""Main module of the project"""

from copy_directory import copy_directory_recursive
from generate_page import generate_pages_recursive


def main():
    """Main function"""
    copy_directory_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()
