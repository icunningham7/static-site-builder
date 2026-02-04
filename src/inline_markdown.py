import re
from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    transformers = [
        lambda ns: split_nodes_delimiter(ns, '`', TextType.CODE),
        lambda ns: split_nodes_delimiter(ns, '**', TextType.BOLD),
        lambda ns: split_nodes_delimiter(ns, '__', TextType.BOLD),
        lambda ns: split_nodes_delimiter(ns, '*', TextType.ITALIC),
        lambda ns: split_nodes_delimiter(ns, '_', TextType.ITALIC),
        split_nodes_image,
        split_nodes_link
    ]

    for transform in transformers:
        nodes = transform(nodes)

    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        if delimiter not in text:
            new_nodes.append(node)
            continue

        parts = text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("A closing delimiter is missing")
        
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                if delimiter in part:
                    inner_nodes = split_nodes_delimiter([TextNode(part, TextType.TEXT)], delimiter, text_type)
                    new_nodes.extend(inner_nodes)
                else:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            node_list.append(old_node)
            continue
        split_nodes = []
        sections = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))", old_node.text)
        for i in range(len(sections)):
            if re.search(r"!\[[^\[\]]*\]\([^\(\)]*\)", sections[i]):
                images = extract_markdown_images(sections[i])
                if images:
                    for alt_text, url in images:
                        split_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            elif sections[i]:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
        node_list.extend(split_nodes)

    return node_list


def split_nodes_link(old_nodes):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            node_list.append(old_node)
            continue
        split_nodes = []
        sections = re.split(r"((?<!!)\[[^\[\]]*\]\([^\(\)]*\))", old_node.text)
        for i in range(len(sections)):
            if re.search(r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)", sections[i]):
                links = extract_markdown_links(sections[i])
                if links:
                    for anchor_text, url in links:
                        split_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            elif sections[i]:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
        node_list.extend(split_nodes)

    return node_list


def extract_markdown_images(text):
    image_links = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_links


def extract_markdown_links(text):
    image_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image_links
