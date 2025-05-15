import unittest
from inline_markdown import ( 
    split_nodes_delimiter, 
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
) 
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    ##################################
    # split_nodes_delimiter Tests
    ##################################
    def test_backtick_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_asterisks_delimiter(self):
        node = TextNode("This is text with a **bolded section** included", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bolded section")
    ##################################
    # extract_markdown_images Tests
    ##################################
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    ##################################
    # extract_markdown_links Tests
    ##################################
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link to jackster](https://www.jackster.com)"
        )
        self.assertListEqual([("link to jackster", "https://www.jackster.com")], matches)
    ##################################
    # split_nodes_image Tests
    ##################################
    def test_split_nodes_image_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode(
            "This node has no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This node has no images", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_image_text_type_code(self):
        node = TextNode(
            "This node is for a code text type",
            TextType.CODE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This node is for a code text type", TextType.CODE)
            ],
            new_nodes,
        )

    def test_split_nodes_image_start_with_image(self):
        node = TextNode(
            "![start with image](https://i.imgur.com/imageatstart.png) and some trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start with image", TextType.IMAGE, "https://i.imgur.com/imageatstart.png"),
                TextNode(" and some trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_back_to_back_image(self):
        node = TextNode(
            "Setting up for some back-to-back images ![image 1](https://i.imgur.com/image1.png)![image 2](https://i.imgur.com/image2.png) and some trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Setting up for some back-to-back images ", TextType.TEXT),
                TextNode("image 1", TextType.IMAGE, "https://i.imgur.com/image1.png"),
                TextNode("image 2", TextType.IMAGE, "https://i.imgur.com/image2.png"),
                TextNode(" and some trailing text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_nodes_multi_nodes(self):
        node1 = TextNode(
            "![start with image](https://i.imgur.com/imageatstart.png) and some trailing text",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This node has no images",
            TextType.TEXT,
        )
        node3 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("start with image", TextType.IMAGE, "https://i.imgur.com/imageatstart.png"),
                TextNode(" and some trailing text", TextType.TEXT),
                TextNode("This node has no images", TextType.TEXT),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()