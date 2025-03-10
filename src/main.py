"""Main module of the project"""
from copy_directory import copy_directory_recursive
from textnode import TextNode
from enums import TextType

def main():
    """Main function
    """
    test_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(test_node)
    copy_directory_recursive('static', 'public')

main()
