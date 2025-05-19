# HTMLNode class represents a "node" in an HTML document tree 
# (like a <p> tag and its contents, or an <a> tag and its contents).
# It can be block level or inline, and is designed to only output HTML.
class HTMLNode():
    # HTMLNode constructor
    # tag (default None): string representation of HTML tag name
    # value (default None): string representation of HTML tag value
    # children (default None): list of HTMLNode objects representing children of this node
    # props (default None): dictionary of key-value pairs representing attributes of HTML tag
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    # method to render the node as HTML output
    # to be overridden in child classes
    def to_html(self):
        raise NotImplementedError("to_html not implemented")
    # method that returns a string that represents the HTML attributes of a node
    def props_to_html(self):
        # if node has no properties, just return empty string
        if self.props is None:
            return ""
        html_attributes = ""
        # for each property associated with the node,
        # format as ' key="value"' (e.g., ' href="https://www.google.com"')
        # and return the resulting string
        for key, value in self.props.items():
            html_attributes += f" {key}=\"{value}\""
        return html_attributes
    # method to return string representaion of HTMLNode object
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

# LeafNode class is an HTMLNode that represents a single HTML tag with no children
class LeafNode(HTMLNode):
    # LeafNode constructor
    # inherits from HTMLNode so uses parent's constructor, but takes "None" as "children" 
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    # method that renders a leaf node as an HTML string
    def to_html(self):
        # if missing value, return error
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        # if tag is None, just return value
        if self.tag is None:
            return self.value
        # otherwise return HTML representation of LeafNode
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    # method to return string representaion of LeafNode object
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"