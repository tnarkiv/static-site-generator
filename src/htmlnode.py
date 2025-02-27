""""This file contains the code for generating HTML nodes"""


class HTMLNode:
    """Class file for HTML Node objects"""

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Converts to HTML"""
        raise NotImplementedError

    def props_to_html(self):
        """Converts properties from dictionary to tag string"""
        html_tag = ""
        for key, value in self.props.items():
            html_tag = html_tag + f' {key}="{value}"'
        return html_tag

    def __eq__(self, node_two):
        """Checks for equivalence of two HTML nodes

        Args:
            node_two (HTMLNode): Second Node
        """
        if (
            self.tag == node_two.tag
            and self.value == node_two.value
            and self.children == node_two.children
            and self.props == node_two.props
        ):
            return True
        else:
            return False

    def __repr__(self):
        print(f"Tag: {self.tag}")
        print(f"Value: {self.value}")
        print(f"Children: {len(self.children)}")
        print("Props: ")
        for key, value in self.props.items():
            print(f"\t{key} : {value}")
        return ""
