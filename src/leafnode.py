"""This file contains the code for leaf nodes"""

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """This class contains leaf nodes, i.e., nodes that don't have any child nodes

    Args:
        HTMLNode (HTMLNode): All leaf nodes are HTML Nodes
    """

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __eq__(self, node_two):
        """Checks for equivalence of two Leaf nodes

        Args:
            node_two (HTMLNode): Second Node
        """
        if (
            self.tag == node_two.tag
            and self.value == node_two.value
            and self.props == node_two.props
        ):
            return True
        else:
            return False

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        else:
            if self.tag is None:
                return self.value
            else:
                props_string = ""
                if self.props is not None:
                    for key, value in self.props.items():
                        props_string = props_string + f' {key}="{value}"'
                tag_string = f"<{self.tag}{props_string}>"
                html_string = f"{tag_string}{self.value}</{self.tag}>"
                return html_string
