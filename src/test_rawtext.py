import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestRawTextToTextNode(unittest.TestCase):

    def test_delimiter_present(self):
        old_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_node = split_nodes_delimiter([old_node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_multiple_delimiter_present(self):
        old_node = TextNode(
            "This is text with a `first code block` and a `second code block`!",
            TextType.TEXT,
        )
        new_node = split_nodes_delimiter([old_node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("first code block", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("second code block", TextType.CODE),
            TextNode("!", TextType.TEXT),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_delimiter_not_present(self):
        old_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_node = split_nodes_delimiter([old_node], "**", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_delimiter_present_at_start(self):
        old_node = TextNode("**Bold** opening", TextType.TEXT)
        new_node = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" opening", TextType.TEXT),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_delimiter_present_at_end(self):
        old_node = TextNode("Closing _italics_", TextType.TEXT)
        new_node = split_nodes_delimiter([old_node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("Closing ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_delimiter_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
