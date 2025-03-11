"""Main module of the project"""

import sys

from copy_directory import copy_directory_recursive
from generate_page import generate_pages_recursive


def main():
    """Main function"""
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_directory_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
