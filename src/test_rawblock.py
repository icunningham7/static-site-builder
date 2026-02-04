import unittest
import unittest.util

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title
from htmlnode import HTMLNode, ParentNode, LeafNode

unittest.util._MAX_LENGTH = 2000

class TestRawMarkdownToBlocks(unittest.TestCase):
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
            ]
        )

    def test_multiple_new_lines_in_markdown_to_blocks(self):
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
                "This is another paragraph with _italic_ text and `code` here",
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        )
      
    def test_no_text_in_markdown_to_blocks(self):
        md = """





"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, 
            []
        )  

    def test_indented_list_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
    - This is an indented list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, 
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n    - This is an indented list\n- with items",
            ]
        )

class TestMarkdownExtractTitle(unittest.TestCase):
    def test_extract_title_standard(self):
        title = extract_title("# This is a heading")
        self.assertEqual(title, "This is a heading")
        
    def test_extract_title_starting_multiline_markdown(self):
        title = extract_title("# This is a heading\nThere are additional lines here.")
        self.assertEqual(title, "This is a heading")
        
    def test_extract_title_ending_multiline_markdown(self):
        title = extract_title("There are additional lines here.\n# This is a heading")
        self.assertEqual(title, "This is a heading")

    def test_extract_title_in_multiline_markdown(self):
        title = extract_title("There are additional lines here.\n# This is a heading\nThe heading is in the middle")
        self.assertEqual(title, "This is a heading")


    def test_extract_title_and_subtitle_in_multiline_markdown(self):
        title = extract_title("There are additional lines here.\n# This is a heading\n## The heading is in the middle")
        self.assertEqual(title, "This is a heading")

    def test_extract_title_with_formatting(self):
        title = extract_title("# This is a **bolded** heading")
        self.assertEqual(title, "This is a **bolded** heading")

    def test_extract_title_no_space_causes_error(self):
        with self.assertRaises(ValueError):
            extract_title("#This is a **bolded** heading")

    def test_extract_title_no_heading_causes_error(self):
        with self.assertRaises(ValueError):
            extract_title(" This is a **bolded** heading")


    def test_extract_title_wrong_h_level_causes_error(self):
        with self.assertRaises(ValueError):
            extract_title("## This is a **bolded** heading")

class TestMarkdownBlockToBlockNode(unittest.TestCase):
    def test_paragraph_block_to_block_node(self):
        block_type = block_to_block_type("This is **bolded** paragraph")
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_heading_block_to_block_node(self):
        block_type = block_to_block_type("# This is **bolded** heading")
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_heading_two_block_to_block_node(self):
        block_type = block_to_block_type("## This is **bolded** heading")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_seven_is_invalid_block_to_block_node(self):
        block_type = block_to_block_type("####### This is **bolded** heading")
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_heading_requires_space_block_to_block_node(self):
        block_type = block_to_block_type("#This is **bolded** heading")
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_heading_requires_char_block_to_block_node(self):
        block_type = block_to_block_type("# ")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code_block_to_block_node(self):
        block_type = block_to_block_type("```\nThis is **bolded** code\n```")
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_multiline_block_to_block_node(self):
        block_type = block_to_block_type("```\nThis is **bolded** code\nIt countains multiple lines\n```")
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_code_requires_newline_block_to_block_node(self):
        block_type = block_to_block_type("```This is **bolded** code\n```")
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_code_requires_ending_newline_block_to_block_node(self):
        block_type = block_to_block_type("```\nThis is **bolded** code```")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote_block_to_block_node(self):
        block_type = block_to_block_type("> This is a **bolded** quote")
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_multiline_block_to_block_node(self):
        block_type = block_to_block_type("> This is a **bolded** quote\n> That goes on multiple lines")
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_space_is_optional_block_to_block_node(self):
        block_type = block_to_block_type(">This is a **bolded** quote\n>That goes on multiple lines")
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list_block_to_block_node(self):
        block_type = block_to_block_type("- This is a unordered list")
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_unordered_list_multiline_block_to_block_node(self):
        block_type = block_to_block_type("- This is a unordered list\n- With multiple lines")
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_unordered_requires_space_list_block_to_block_node(self):
        block_type = block_to_block_type("-This is a unordered list")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_multiple_items_block_to_block_node(self):
        block_type = block_to_block_type("1. This is an ordered list\n2. It has multiple items")
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_starts_at_one_block_to_block_node(self):
        block_type = block_to_block_type("0. This is an ordered list")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_cannot_skip_block_to_block_node(self):
        block_type = block_to_block_type("1. This is an ordered list\n3. It has multiple items")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_requires_space_block_to_block_node(self):
        block_type = block_to_block_type("1.This is an ordered list")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_requires_period_block_to_block_node(self):
        block_type = block_to_block_type("1 This is an ordered list")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

        
class TestMarkdownBlockToHTMLNode(unittest.TestCase):
    def test_paragraph_markdown_to_html_node(self):
        block = markdown_to_html_node("This is **bolded** paragraph")
        parent_node = ParentNode("div", [ParentNode("p", [LeafNode(None,"This is "), LeafNode("b", "bolded"), LeafNode(None, " paragraph")])])
        self.assertEqual(block, parent_node)

    def test_heading_markdown_to_html_node(self):
        block = markdown_to_html_node("# This is **bolded** heading")
        parent_node = ParentNode("div", [ParentNode("h1", [LeafNode(None, "This is "), LeafNode("b", "bolded"), LeafNode(None, " heading")])])
        self.assertEqual(block, parent_node)

    def test_code_markdown_to_html_node(self):
        block = markdown_to_html_node("```\nThis is **bolded** code\nIt countains multiple lines\n```")
        parent_node = ParentNode("div", [ParentNode("pre", [ParentNode("code", [LeafNode(None,"This is **bolded** code\nIt countains multiple lines")])])])
        self.assertEqual(block, parent_node)
        
    def test_quote_markdown_to_html_node(self):
        block = markdown_to_html_node(">This is a **bolded** quote\n>That goes on multiple lines")
        parent_node = ParentNode("div", [ParentNode("blockquote", [LeafNode(None, "This is a "), LeafNode("b", "bolded"), LeafNode(None, " quote That goes on multiple lines")])])
        self.assertEqual(block, parent_node)

    def test_quote_with_space_markdown_to_html_node(self):
        block = markdown_to_html_node("> This is a **bolded** quote\n> That goes on multiple lines")
        parent_node = ParentNode("div", [ParentNode("blockquote", [LeafNode(None, "This is a "), LeafNode("b", "bolded"), LeafNode(None, " quote That goes on multiple lines")])])
        self.assertEqual(block, parent_node)
        
    def test_unordered_list_block_to_block_node(self):
        block = markdown_to_html_node("- This is a unordered list")
        parent_node = ParentNode("div", [ParentNode("ul", [ParentNode('li', [LeafNode(None,"This is a unordered list")])])])
        self.assertEqual(block, parent_node)
                
    def test_unordered_multiple_list_block_to_block_node(self):
        block = markdown_to_html_node("- This is a unordered list\n- With multiple lines")
        parent_node = ParentNode("div", [ParentNode("ul", [ParentNode('li', [LeafNode(None, "This is a unordered list")]), ParentNode('li', [LeafNode(None,"With multiple lines")])])])
        self.assertEqual(block, parent_node)

    def test_ordered_list_items_block_to_block_node(self):
        block = markdown_to_html_node("1. This is an ordered list")
        parent_node = ParentNode("div", [ParentNode("ol", [ParentNode('li', [LeafNode(None, "This is an ordered list")])])])
        self.assertEqual(block, parent_node)

    def test_ordered_list_multiple_items_block_to_block_node(self):
        block = markdown_to_html_node("1. This is an ordered list\n2. It has multiple items")
        parent_node = ParentNode("div", [ParentNode("ol", [ParentNode('li', [LeafNode(None, "This is an ordered list")]), ParentNode("li", [LeafNode(None,"It has multiple items")])])])
        self.assertEqual(block, parent_node)


    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
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