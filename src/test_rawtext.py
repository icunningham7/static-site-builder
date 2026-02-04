import unittest

from inline_markdown import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestRawTextToTextNode(unittest.TestCase):

    def test_text_to_textnodes(self):
        new_node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected_nodes = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])


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
        new_node = split_nodes_delimiter([old_node], "**", TextType.BOLD)
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

class TestRawTextToImageNode(unittest.TestCase):
    def test_single_image_markdown(self):
        old_node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)!",
            TextType.TEXT,
        )
        new_node = split_nodes_image([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("!", TextType.TEXT, None),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_multiple_image_markdown(self):
        old_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([old_node])
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_link_is_not_image_markdown(self):
        old_node = TextNode(
            "This is text with a link [rick roll](https://i.imgur.com/aKaOqIh.gif)!",
            TextType.TEXT,
        )
        new_node = split_nodes_image([old_node])
        expected_nodes = [
            TextNode("This is text with a link [rick roll](https://i.imgur.com/aKaOqIh.gif)!", TextType.TEXT, None)
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_no_alt_text_image_markdown(self):
        old_node = TextNode(
            "This is text with a ![](https://i.imgur.com/aKaOqIh.gif)!",
            TextType.TEXT,
        )
        new_node = split_nodes_image([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("!", TextType.TEXT, None),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_no_url_image_markdown(self):
        old_node = TextNode(
            "This is text with a ![rick roll]()!",
            TextType.TEXT,
        )
        new_node = split_nodes_image([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.IMAGE, ""),
            TextNode("!", TextType.TEXT, None),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_empty_image_markdown(self):
        old_node = TextNode(
            "This is text with a ![]()!",
            TextType.TEXT,
        )
        new_node = split_nodes_image([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("", TextType.IMAGE, ""),
            TextNode("!", TextType.TEXT, None),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

class TestRawTextToLinkNode(unittest.TestCase):
    def test_single_link_markdown(self):
        old_node = TextNode(
            "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)!",
            TextType.TEXT,
        )
        new_node = split_nodes_link([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("!", TextType.TEXT, None),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_multiple_link_markdown(self):
        old_node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_image_is_not_link_markdown(self):
        old_node = TextNode(
            "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)!",
            TextType.TEXT,
        )
        new_node = split_nodes_link([old_node])
        expected_nodes = [
            TextNode("This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)!", TextType.TEXT, None)
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_no_anchor_text_link_markdown(self):
        old_node = TextNode(
            "This is text with a [](https://i.imgur.com/aKaOqIh.gif)!",
            TextType.TEXT,
        )
        new_node = split_nodes_link([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("!", TextType.TEXT, None),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_no_url_link_markdown(self):
        old_node = TextNode(
            "This is text with a [rick roll]()!",
            TextType.TEXT,
        )
        new_node = split_nodes_link([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.LINK, ""),
            TextNode("!", TextType.TEXT, None),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

    def test_empty_link_markdown(self):
        old_node = TextNode(
            "This is text with a []()!",
            TextType.TEXT,
        )
        new_node = split_nodes_link([old_node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("", TextType.LINK, ""),
            TextNode("!", TextType.TEXT, None),
        ]
        for index, node in enumerate(new_node):
            self.assertEqual(node, expected_nodes[index])

class TestRawTextImageMarkdownExtraction(unittest.TestCase):

    def test_single_image_markdown(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)!"
        image_content = extract_markdown_images(text)
        self.assertEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")], image_content
        )

    def test_multiple_image_markdown(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image_content = extract_markdown_images(text)
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            image_content,
        )

    def test_no_alt_image_markdown(self):
        text = "This is an image with no alt text ![](https://i.imgur.com/aKaOqIh.gif)!"
        image_content = extract_markdown_images(text)
        self.assertEqual([("", "https://i.imgur.com/aKaOqIh.gif")], image_content)

    def test_no_url_image_markdown(self):
        text = "This is an image with no url text ![forgot the url]()!"
        image_content = extract_markdown_images(text)
        self.assertEqual([("forgot the url", "")], image_content)

    def test_empty_image_markdown(self):
        text = "This is image markdown with no alt text or url ![]()!"
        image_content = extract_markdown_images(text)
        self.assertEqual([("", "")], image_content)

    def test_link_is_not_image_markdown(self):
        text = "This is a [link](https://www.google.com) that shouldn't be picked up as an image"
        image_content = extract_markdown_images(text)
        self.assertEqual([], image_content)

    def test_missing_open_bracket_image_markdown(self):
        text = "This is text with a !rick roll](https://i.imgur.com/aKaOqIh.gif)!"
        image_content = extract_markdown_images(text)
        self.assertEqual([], image_content)

    def test_missing_closing_bracket_image_markdown(self):
        text = "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif)!"
        image_content = extract_markdown_images(text)
        self.assertEqual([], image_content)

    def test_missing_open_parenthesis_image_markdown(self):
        text = "This is text with a ![rick roll]https://i.imgur.com/aKaOqIh.gif)!"
        image_content = extract_markdown_images(text)
        self.assertEqual([], image_content)

    def test_missing_close_parenthesis_image_markdown(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif!"
        image_content = extract_markdown_images(text)
        self.assertEqual([], image_content)

class TestRawTextLinkMarkdownExtraction(unittest.TestCase):

    def test_single_link_markdown(self):
        text = "This is text with a link [rick roll](https://i.imgur.com/aKaOqIh.gif)!"
        link_content = extract_markdown_links(text)
        self.assertEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")], link_content
        )

    def test_multiple_link_markdown(self):
        text = "This is text with two links [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        link_content = extract_markdown_links(text)
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            link_content,
        )

    def test_no_anchor_link_markdown(self):
        text = "This is a link with no anchor text [](https://i.imgur.com/aKaOqIh.gif)!"
        link_content = extract_markdown_links(text)
        self.assertEqual([("", "https://i.imgur.com/aKaOqIh.gif")], link_content)

    def test_no_url_link_markdown(self):
        text = "This is a link with no url [forgot the url]()!"
        link_content = extract_markdown_links(text)
        self.assertEqual([("forgot the url", "")], link_content)

    def test_empty_link_markdown(self):
        text = "This is link markdown with no anchor text or url []()!"
        link_content = extract_markdown_links(text)
        self.assertEqual([("", "")], link_content)

    def test_image_is_not_link_markdown(self):
        text = "This is an image ![link](https://i.imgur.com/aKaOqIh.gif) that shouldn't be picked up as a link."
        link_content = extract_markdown_links(text)
        self.assertEqual([], link_content)

    def test_missing_open_bracket_link_markdown(self):
        text = "This is text with a rick roll](https://i.imgur.com/aKaOqIh.gif)!"
        link_content = extract_markdown_links(text)
        self.assertEqual([], link_content)

    def test_missing_closing_bracket_link_markdown(self):
        text = "This is text with a [rick roll(https://i.imgur.com/aKaOqIh.gif)!"
        link_content = extract_markdown_links(text)
        self.assertEqual([], link_content)

    def test_missing_open_parenthesis_link_markdown(self):
        text = "This is text with a [rick roll]https://i.imgur.com/aKaOqIh.gif)!"
        link_content = extract_markdown_links(text)
        self.assertEqual([], link_content)

    def test_missing_close_parenthesis_link_markdown(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif!"
        link_content = extract_markdown_links(text)
        self.assertEqual([], link_content)


if __name__ == "__main__":
    unittest.main()
