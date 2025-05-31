from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# function that takes a single block of markdown text as input and 
# returns the BlockType representing the type of block it is
def block_to_blocktype(block_markdown):
    # check if any of the first 1 though 6 characters of the block
    # start with #s followed by a space, if so, it's a heading
    if block_markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # split the markdown into lines by splitting on each newline found in the string
    block_lines = block_markdown.split("\n")
    # if the block has multiple lines and the first line and last line start with 
    # three backticks, then it's a code block
    if (len(block_lines) > 1 
        and block_lines[0].startswith("```") 
        and block_lines[-1].startswith("```")):
        return BlockType.CODE
    # if the block starts with a > and each line in the block starts with >
    # then it's a quote
    if block_markdown.startswith(">"):
        for block_line in block_lines:
            if not block_line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    # if the block starts with a dash followed by space and 
    # each line in the block starts with a dash followed by a space
    # then it's an unordered list
    if block_markdown.startswith("- "):
        for block_line in block_lines:
            if not block_line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    # if the block starts with a 1. followed by space and 
    # each line in the block starts with the next number in series 
    # followed by a space then it's an ordered list
    if block_markdown.startswith("1. "):
        i = 1
        for block_line in block_lines:
            if not block_line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    # return as a paragraph if none of the other conditions met above
    return BlockType.PARAGRAPH

# function that takes a raw markdown string (representing a full document) 
# as input and returns a list of "block" strings
def markdown_to_blocks(markdown):
    # split the markdown into blocks that are defined as a newline followed by
    # another newline
    blocks = markdown.split("\n\n")
    new_blocks = []
    # loop through each block after the split
    for block in blocks:
        # strip any leading or trailing whitespace
        block = block.strip()
        # don't allow any empty blocks to be captured
        if block == "":
            continue
        # add the processed block to the list of new blocks to return
        new_blocks.append(block)
    # return the list of new blocks
    return new_blocks

# function that converts a full markdown document into a single
# parent HTMLNode that contains many child HTMLNode objects representing
# the nested elemments
def markdown_to_html_node(markdown):
    block_html_nodes = []
    # split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    # loop over each block
    for block in blocks:
        # determine the type of block
        block_type = block_to_blocktype(block)
        # get the HTML node associated with the block type
        block_html_node = None
        match block_type:
            case BlockType.HEADING:
                block_html_node = create_heading_html(block)
            case BlockType.CODE:
                block_html_node = create_codeblock_html(block)
            case BlockType.QUOTE:
                block_html_node = create_quote_html(block)
            case BlockType.UNORDERED_LIST:
                block_html_node = create_list_html(block, ordered = False)
            case BlockType.ORDERED_LIST:
                block_html_node = create_list_html(block, ordered = True)
            case _:
                block_html_node = create_paragraph_html(block)
        block_html_nodes.append(block_html_node)
    return ParentNode("div", block_html_nodes)

# function to create a heading HTML node from heading markup block
def create_heading_html(heading_block_text):
    # find the first space in the markup to determine where the heading begins
    first_space_index = heading_block_text.find(" ")
    # get the heading characters by grabbing all up to the position of the 
    # first space
    heading_chars = heading_block_text[:first_space_index]
    # get the remaining text after the heading characters and the space
    heading_text = heading_block_text[first_space_index + 1:]
    # get the count of the heading characters to determine the heading level
    heading_chars_count = heading_chars.count("#")
    # format the heading level (e.g., h1, h2, etc.)
    heading_level = f"h{heading_chars_count}"
    # split the heading text into lines by splitting on the newlines in the text
    heading_lines = heading_text.split("\n")
    # join the individual lines back into a string with space-delimiter and strip
    # leading and trailing spaces
    heading = " ".join(heading_lines).strip()
    # search for any child inline HTML nodes in the heading
    children = text_to_children(heading)
    # return the heading as a parent HTML node
    return ParentNode(tag = heading_level, children = children)

# function to create a code block HTML node from code block markup
def create_codeblock_html(codeblock_text):
    # get the lines in the code block by splitting on the newlines in the text
    codeblock_lines = codeblock_text.split("\n")
    # remove the first and last lines (which will have the ```)
    code = codeblock_lines[1:-1]
    # join the individual lines back into a string with newlines
    code = "\n".join(code) + "\n"
    # create a code type text node out of the code text
    code_text_node = TextNode(text = code, text_type = TextType.CODE)
    # create a child leaf HTML node out of the text node
    child = text_node_to_html_node(code_text_node)
    # link the child node to a new parent HTML node with a "pre" tag and
    # return it
    return ParentNode("pre", [child])

# function to create a blockquote HTML node from quote markup block
def create_quote_html(quote_text):
    clean_quote_lines = []
    # get the lines in the quote block by splitting on newlines in the text
    quote_lines = quote_text.split("\n")
    # remove the ">" at the start of each line and add to list of clean lines
    for line in quote_lines:
        clean_line = line[1:]
        clean_quote_lines.append(clean_line)
    # join the individual lines back into a string with space-delimiter and strip
    # leading and trailing spaces
    quote = " ".join(clean_quote_lines).strip()
    # quote = "\n".join(clean_quote_lines)
    # search for any child inline HTML nodes in the quote
    children = text_to_children(quote)
    # return the quote as a parent HTML node
    return ParentNode(tag = "blockquote", children = children)

# function to create a list HTML node from list markup block
def create_list_html(list_text, ordered):
    list_item_html_nodes = []
    list_item_start_index = list_text.find(" ") + 1
    list_tag = "ul"
    if ordered:
        list_tag = "ol"
    #split the list into lines
    list_items = list_text.split("\n")
    for list_item in list_items:
        list_item_text = list_item[list_item_start_index:]
        children = text_to_children(list_item_text)
        list_item_html_node = ParentNode(tag = "li", children = children)
        list_item_html_nodes.append(list_item_html_node)
    return ParentNode(tag = list_tag, children = list_item_html_nodes)

# function to create a paragraph HTML node from paragraph markup block
def create_paragraph_html(paragraph_text):
    # split the paragraph text into lines using newline characters
    paragraph_lines = paragraph_text.split("\n")
    # join the lines into a string without newlines by joining on space
    # strip any leading or trailing spaces
    paragraph = " ".join(paragraph_lines).strip()
    # search for any child inline HTML nodes in the paragraph
    children = text_to_children(paragraph)
    # return the paragraph as a parent HTML node
    return ParentNode(tag = "p", children = children)

# does not work with code block type  
def text_to_children(text):
    html_nodes = []
    text_nodes =  text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes
    