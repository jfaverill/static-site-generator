from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
# from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from markdown_blocks import create_heading_html

def main():
    # tn = TextNode("This is some anchor text",TextType.LINK , "https://www.boot.dev")
    # print(tn)

    # hn = HTMLNode("p", "This is a paragraph", None, {"href": "https://www.google.com", "target": "_blank"})
    # print(hn)

    # ln = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    # print(ln)

    # html = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
    # print(html)

    # html = LeafNode("p", "This is a paragraph of text.").to_html()
    # print(html)

    # node = TextNode("This is text with a `code block` word", TextType.TEXT)
    # node2 = TextNode("`Code block` is here so `we need` it", TextType.TEXT)
    # node3 = TextNode("Okay so `code block` is here so we need `it`", TextType.TEXT)
    # node4 = TextNode("This one has `a` problem", TextType.TEXT)
    # new_nodes = split_nodes_delimiter([node, node2, node3, node4], "`", TextType.CODE)
    # print(new_nodes)

    # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ![ben kenob](https://konami.jpeg)"
    # results = extract_markdown_images(text)
    # print(results)

    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # results = extract_markdown_links(text)
    # print(results)
    heading_text = """
# This is a _heading_ that will
be split over a great, great
**many** lines just to see how this whole
heading gets handled
"""
    node = create_heading_html(heading_text)
    print(node.to_html())

main()