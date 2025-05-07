from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid text type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            delimiter_count = old_node.text.count(delimiter)
            if not (delimiter_count % 2 == 0):
                raise Exception("invalid markup: no closing delimiter")
            node_parts = old_node.text.split(delimiter)
            for i in range(len(node_parts)):
                if i % 2 == 1:
                    new_node = TextNode(node_parts[i], text_type)
                else:
                    new_node = TextNode(node_parts[i], old_node.text_type)
                if new_node.text != "":
                    new_nodes.append(new_node)
    return new_nodes

        
def main():
    tn = TextNode("This is some anchor text",TextType.LINK , "https://www.boot.dev")
    print(tn)

    hn = HTMLNode("p", "This is a paragraph", None, {"href": "https://www.google.com", "target": "_blank"})
    print(hn)

    ln = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(ln)

    html = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
    print(html)

    html = LeafNode("p", "This is a paragraph of text.").to_html()
    print(html)

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    node2 = TextNode("`Code block` is here so `we need` it", TextType.TEXT)
    node3 = TextNode("Okay so `code block` is here so we need `it`", TextType.TEXT)
    node4 = TextNode("This one has `a` problem", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node, node2, node3, node4], "`", TextType.CODE)
    print(new_nodes)

main()