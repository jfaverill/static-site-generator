import unittest
from markdown_blocks import markdown_to_blocks, block_to_blocktype, BlockType

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
        block_md = "``` This should end up being a paragraph```"
        block_type = block_to_blocktype(block_md)
        self.assertEqual(BlockType.CODE, block_type)
