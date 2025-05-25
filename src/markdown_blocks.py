from enum import Enum

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