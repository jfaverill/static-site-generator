import unittest
from inline_markdown import ( 
    split_nodes_delimiter, 
    extract_markdown_images,
    extract_markdown_links
) 
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_backtick_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_asterisks_delimiter(self):
        node = TextNode("This is text with a **bolded section** included", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bolded section")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link to jackster](https://www.jackster.com)"
        )
        self.assertListEqual([("link to jackster", "https://www.jackster.com")], matches)

if __name__ == "__main__":
    unittest.main()