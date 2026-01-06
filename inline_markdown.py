from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            node_list.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("A closing delimiter is missing")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        node_list.extend(split_nodes)

    return node_list
