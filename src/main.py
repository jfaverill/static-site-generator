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

main()