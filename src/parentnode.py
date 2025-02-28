"""This file contains the code for Parent Nodes"""

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """Class file for Parent Nodes, i.e., nodes having children

    Args:
        HTMLNode (HTMLNode): All parent nodes are HTML Nodes
    """

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __eq__(self, node_two):
        if (
            self.tag == node_two.tag
            and self.children == node_two.children
            and self.props == node_two.props
        ):
            return True
        else:
            return False

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent nodes must have a tag")
        elif self.children is None:
            raise ValueError("parent nodes must have child nodes")
        else:
            children_string = ""
            for child_node in self.children:
                children_string = children_string + child_node.to_html()
            return f"<{self.tag}>{children_string}</{self.tag}>"
