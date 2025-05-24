from textnode import TextNode, TextType
import re

# function that takes a list of "old nodes", a delimiter, and a text type 
# and returns a new list of nodes, where any "text" type nodes in the input 
# list are (potentially) split into multiple nodes based on the syntax.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # loop through all old nodes in the old nodes list
    for old_node in old_nodes:
        # if the old node is a text type node, then just append it to
        # the new nodes list
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            # otherwise...
            # split the text of the old node by the incoming delimiter
            node_parts = old_node.text.split(delimiter)
            # if the node has an opening and closing delimiter, then 
            # it should always have an odd number of node parts/sections after the split
            # if it has an even number of sections, then it's missing a closing delimiter
            # so raise an exception
            if len(node_parts) % 2 == 0:
                raise Exception("invalid markup: no closing delimiter") 
            # loop through each node part...
            for i in range(len(node_parts)):
                # if it's an odd node part, then it's a non-text type node so create that
                # using the incoming text type
                if i % 2 == 1:
                    new_node = TextNode(node_parts[i], text_type)
                else:
                    # otherwise it's a text type node, so create that from the original
                    # text type (which will be be a "text" text type)
                    new_node = TextNode(node_parts[i], old_node.text_type)
                # if the node's text is not an empty string, then add to the new nodes list
                if new_node.text != "":
                    new_nodes.append(new_node)
    # return the list of new nodes
    return new_nodes

def extract_markdown_images(text):
    image_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_matches

def extract_markdown_links(text):
    link_matches = re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        image_matches = extract_markdown_images(old_node.text)
        if old_node.text_type != TextType.TEXT or len(image_matches) == 0:
            new_nodes.append(old_node)
        else:
            old_node_text = old_node.text
            for image_match in image_matches:
                alt_text, url = image_match
                node_parts = old_node_text.split(f"![{alt_text}]({url})", maxsplit = 1)
                text_node = TextNode(node_parts[0], old_node.text_type)
                image_node = TextNode(alt_text, TextType.IMAGE, url)
                if text_node.text != "":
                    new_nodes.append(text_node)
                new_nodes.append(image_node)
                old_node_text = old_node_text.replace(f"{node_parts[0]}![{alt_text}]({url})", "")
            # get any remaining/trailing text
            if len(old_node_text) > 0:
                new_nodes.append(TextNode(old_node_text, old_node.text_type))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        link_matches = extract_markdown_links(old_node.text)
        if old_node.text_type != TextType.TEXT or len(link_matches) == 0:
            new_nodes.append(old_node)
        else:
            old_node_text = old_node.text
            for link_match in link_matches:
                link_text, url = link_match
                node_parts = old_node_text.split(f"[{link_text}]({url})", maxsplit = 1)
                text_node = TextNode(node_parts[0], old_node.text_type)
                link_node = TextNode(link_text, TextType.LINK, url)
                if text_node.text != "":
                    new_nodes.append(text_node)
                new_nodes.append(link_node)
                old_node_text = old_node_text.replace(f"{node_parts[0]}[{link_text}]({url})", "")
            # get any remaining/trailing text
            if len(old_node_text) > 0:
                new_nodes.append(TextNode(old_node_text, old_node.text_type))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes