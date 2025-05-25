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
                raise ValueError("invalid markup: no closing delimiter") 
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

# function to extract image data from markdown text
def extract_markdown_images(text):
    # use regex to capture matches of the markdown pattern for images and 
    # return them as a list of tuples
    image_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_matches

# function to extract link data from markdown text
def extract_markdown_links(text):
    # use regex to capture matches of the markdown pattern for links and 
    # return them as a list of tuples
    link_matches = re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_matches

# function that takes a list of "old nodes", extracts any images from the 
# markup and returns a new list of text and image nodes, 
# where any "text" type nodes in the input list are (potentially) split 
# into multiple nodes based on the syntax.
def split_nodes_image(old_nodes):
    new_nodes = []
    # loop through all old nodes in the old nodes list
    for old_node in old_nodes:
        # extract any images found in the markup for the text node
        image_matches = extract_markdown_images(old_node.text)
        # if the old node is a text type node, 
        # or there are no images found in the text markup
        # then just append it to the new nodes list
        if old_node.text_type != TextType.TEXT or len(image_matches) == 0:
            new_nodes.append(old_node)
        else:
            # otherwise...
            # save off the text from the old node
            old_node_text = old_node.text
            # loop through all images found in the markup
            for image_match in image_matches:
                # tuple unpack the alt text and url from the current image
                alt_text, url = image_match
                # do a split on the old node text with a max split of 1 to get the
                # text before the image and after the image
                node_parts = old_node_text.split(f"![{alt_text}]({url})", maxsplit = 1)
                # if a split on the image was successful, it will create 2 node parts
                # one before the image and another after the image
                # if there aren't 2 node parts, then raise an exception
                if len(node_parts) != 2:
                    raise ValueError("invalid markup: image secion not fully closed")
                # create the text node from the first node part
                text_node = TextNode(node_parts[0], old_node.text_type)
                # create the image node from the alt text and url of the image
                image_node = TextNode(alt_text, TextType.IMAGE, url)
                # if the text node create doesn't have empty string for it's text 
                # attribute then add it to the new nodes list
                if text_node.text != "":
                    new_nodes.append(text_node)
                # add the image node to the new nodes list
                new_nodes.append(image_node)
                # set the old node text variable to the text after the image
                old_node_text = node_parts[1]
            # get any remaining/trailing text and add it as a text node to 
            # the new nodes list
            if len(old_node_text) > 0:
                new_nodes.append(TextNode(old_node_text, old_node.text_type))
    # return the list of new nodes
    return new_nodes

# function that takes a list of "old nodes", extracts any links from the 
# markup and returns a new list of text and link nodes, 
# where any "text" type nodes in the input list are (potentially) split 
# into multiple nodes based on the syntax.
def split_nodes_link(old_nodes):
    new_nodes = []
    # loop through all old nodes in the old nodes list
    for old_node in old_nodes:
        # extract any links found in the markup for the text node
        link_matches = extract_markdown_links(old_node.text)
        # if the old node is a text type node, 
        # or there are no links found in the text markup
        # then just append it to the new nodes list
        if old_node.text_type != TextType.TEXT or len(link_matches) == 0:
            new_nodes.append(old_node)
        else:
            # otherwise...
            # save off the text from the old node
            old_node_text = old_node.text
            # loop through all links found in the markup
            for link_match in link_matches:
                # tuple unpack the link text and url from the current link
                link_text, url = link_match
                # do a split on the old node text with a max split of 1 to get the
                # text before the link and after the link
                node_parts = old_node_text.split(f"[{link_text}]({url})", maxsplit = 1)
                # if a split on the link was successful, it will create 2 node parts
                # one before the link and another after the link
                # if there aren't 2 node parts, then raise an exception
                if len(node_parts) != 2:
                    raise ValueError("invalid markup: link secion not fully closed")
                # create the text node from the first node part
                text_node = TextNode(node_parts[0], old_node.text_type)
                # create the link node from the link text and url of the link
                link_node = TextNode(link_text, TextType.LINK, url)
                # if the text node create doesn't have empty string for it's text 
                # attribute then add it to the new nodes list
                if text_node.text != "":
                    new_nodes.append(text_node)
                # add the link node to the new nodes list
                new_nodes.append(link_node)
                # set the old node text variable to the text after the link
                old_node_text = node_parts[1]
            # get any remaining/trailing text and add it as a text node to 
            # the new nodes list
            if len(old_node_text) > 0:
                new_nodes.append(TextNode(old_node_text, old_node.text_type))
    # return the list of new nodes
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes