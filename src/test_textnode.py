import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node = TextNode("Test for TextType inequality", TextType.NORMAL)
        node2 = TextNode("Test for TextType inequality", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        node = TextNode("Test for URL inequality", TextType.ITALIC, "www.google.com")
        node2 = TextNode("Test for URL inequality", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()