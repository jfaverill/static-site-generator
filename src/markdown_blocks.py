from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERDED_LIST = "ordered_list"

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
        return BlockType.ORDERDED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        new_blocks.append(block)
    return new_blocks