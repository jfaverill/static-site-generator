from textnode import TextNode, TextType
import re

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

def extract_markdown_images(text):
    image_matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return image_matches

def extract_markdown_links(text):
    link_matches = re.findall(r"[^!]\[(.+?)\]\((.+?)\)", text)
    return link_matches