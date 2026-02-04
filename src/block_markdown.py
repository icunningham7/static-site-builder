import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    markdown_blocks = [ block.strip() for block in markdown.split('\n\n') if block.strip() ]
    return markdown_blocks

def extract_title(markdown):
    raw_matches = re.search(r"(?<!#)# .+", markdown)
    if not raw_matches:
        raise ValueError("markdown does not contain a title")
    title = raw_matches.group(0)[2:].strip()
    return title

def block_to_block_type(block):
    lines = block.split("\n")

    if len(lines) == 1 and re.match(r"#{1,6} .+", block):
        return BlockType.HEADING
    if len(lines) >= 3 and re.match(r"```", lines[0]) and re.match(r"```$", lines[-1]):
        return BlockType.CODE
    if re.match(r"> ?.*", block):
        for line in lines:
            if not re.match(r"> ?.*", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if re.match(r"- ", block):
        for line in lines:
            if not re.match(r"- ", line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if re.match(r"1. ", block):
        i = 1
        for line in lines:
            if not re.match(rf"{i}\. ", line):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        child_nodes.append(block_to_html_node(block))
    return ParentNode("div", child_nodes)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_nodes(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_nodes(block)
    raise ValueError('invalid block type')

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def paragraph_to_html_node(block):
    raw_lines = block.split("\n")
    paragraph = " ".join(raw_lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    match_group = re.search(r"(#{1,6} )(.+)", block)
    heading_level = len(match_group.group(1)) - 1
    heading = text_to_children(match_group.group(2))
    return ParentNode(f'h{heading_level}', heading)

def code_to_html_node(block):
    match_group = re.search(r"```(?:\n)?(.*?)```", block, re.DOTALL)
    text = match_group.group(1)
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode('pre', [code])

def quote_to_html_node(block):
    raw_lines = block.split("\n")
    new_lines = []
    for raw_line in raw_lines:
        text = raw_line.removeprefix(">").strip()
        new_lines.append(text)
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def unordered_list_to_html_nodes(block):
    raw_lines = block.split("\n")
    list_nodes = []
    for raw_line in raw_lines:
        text = raw_line.removeprefix("-").strip()
        children = text_to_children(text)
        list_nodes.append(ParentNode("li", children))

    return ParentNode("ul", list_nodes)


def ordered_list_to_html_nodes(block):
    raw_lines = block.split("\n")
    list_nodes = []
    for raw_line in raw_lines:
        parts = raw_line.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        list_nodes.append(ParentNode("li", children))

    return ParentNode("ol", list_nodes)
