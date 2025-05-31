from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
# from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from markdown_blocks import (create_heading_html, 
                             create_codeblock_html, 
                             create_quote_html,
                             create_list_html,
                             create_paragraph_html)

def main():
    heading_text = """
###### This is a _heading_ that will
be split over a great, great
**many** lines just to see how this whole
heading gets handled
"""
    node = create_heading_html(heading_text)
    print(node.to_html())

    md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
    node = create_codeblock_html(md)
    print(node.to_html())

    quote_text = """
>Ask not what your country can
>do for **you**.
>Ask Rather.
>Ask Dan Rather.
>He'll know.
"""
    node = create_quote_html(quote_text)
    print(node.to_html())

    quote_text = ">This is\n>another _important_ quote\n>that we **need to add** for posterity"
    node = create_quote_html(quote_text)
    print(node.to_html())

    ul_text = "- First unordered list item\n- Second item\n- and this is the third item"
    node = create_list_html(ul_text, False)
    print(node.to_html())

    ol_text = "1. Ask not what _your country_ can\n2. do for **you**.\n3. Ask Dan Rather."

    node = create_list_html(ol_text, True)
    print(node.to_html())

    md = """
This is **bolded** paragraph
text in a p
tag here
"""
    node = create_paragraph_html(md)
    print(node.to_html())

    md = "This is another paragraph with _italic_ text and `code` here"
    node = create_paragraph_html(md)
    print(node.to_html())

main()