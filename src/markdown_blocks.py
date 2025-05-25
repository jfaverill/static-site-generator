from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(block_markdown):
    heading_match = re.search(r"^#{1,6} ", block_markdown)
    if heading_match:
        return BlockType.HEADING
    #code_block_match = re.search(r"^```.+```$", block_markdown)
    if block_markdown.startswith("```") and block_markdown.endswith("```"):
        return BlockType.CODE
    if block_markdown.startswith(">"):
        return BlockType.QUOTE
    if block_markdown.startswith("- "):
        return BlockType.UNORDERED_LIST
    if block_markdown.startswith("1. "):
        return BlockType.ORDERED_LIST
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