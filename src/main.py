"""Main module of the project"""
from textnode import TextNode, TextType

def main():
    """Main function
    """
    test_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(test_node.__repr__())
main()
