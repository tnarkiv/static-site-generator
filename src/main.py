"""Main module of the project"""
from textnode import TextNode
from enums import TextType

def main():
    """Main function
    """
    test_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(test_node)
main()
