import unittest
from markdown_blocks import (markdown_to_blocks, 
                             block_to_blocktype, 
                             BlockType,
                             markdown_to_html_node)

class TestMarkdownToHTML(unittest.TestCase):
    ##################################
    # markdown_to_blocks Tests
    ##################################
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    ##################################
    # block_to_blocktype Tests
    ##################################
    def test_block_to_blocktype_heading_3(self):
        block_md = "### This is a heading 3"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_blocktype_heading_1(self):
        block_md = "# This is a heading 1"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_blocktype_heading_6(self):
        block_md = "###### This is a heading 6"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_blocktype_heading_7(self):
        block_md = "####### This should end up being a paragraph"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_blocktype_codeblock(self):
        block_md = "```\nThis is a code block\n```"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.CODE, block_type)
    
    def test_block_to_blocktype_quote(self):
        block_md = "> 1st quote line\n> 2nd quote line\n> 3rd quote line"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_blocktype_unordered_list(self):
        block_md = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_blocktype_ordered_list(self):
        block_md = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

#     def test_paragraphs(self):
#         md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# """

#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
#         )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
