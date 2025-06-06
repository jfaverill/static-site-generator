# from textnode import TextNode, TextType
# from htmlnode import HTMLNode, LeafNode
# from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
# from markdown_blocks import (create_heading_html, 
#                              create_codeblock_html, 
#                              create_quote_html,
#                              create_list_html,
#                              create_paragraph_html)
import os, shutil

def copy_static(source_path):
    if source_path == "public":
        if os.path.exists(source_path):
            shutil.rmtree(source_path)
            os.mkdir(source_path)
        else:
            os.mkdir(source_path)
        source_path = "static"

    dir_items = os.listdir(source_path)
    for item in dir_items:
        to_copy = os.path.join(source_path, item)
        print(to_copy)
        #shutil.copy(to_copy, "public")
        if not os.path.isfile(to_copy):
            new_dir = os.path.join("public", to_copy.replace("static/", ""))
            os.mkdir(new_dir)
            copy_static(to_copy)
        else:
            shutil.copy(to_copy, os.path.join("public", to_copy.replace("static/", "")))

def main():
    copy_static(source_path = "public")

main()