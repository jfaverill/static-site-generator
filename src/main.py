from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode

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