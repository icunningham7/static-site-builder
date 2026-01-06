import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    ###     HTMLNode    ####
    def test_empty_htmlnode(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_tag(self):
        node = HTMLNode("a")
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_value(self):
        node = HTMLNode(value="Here's a website to try")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "Here's a website to try")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_children(self):
        pass

    def test_props(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(
            node.props,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

    def test_to_html(self):
        node = HTMLNode(
            "a",
            "Here's a website to try",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        # self.assertRaises(ValueError, node.to_html) # Alternative to current (using manager style)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    ###     LeafNode    ####
    def test_leaf_no_value(self):
        node = LeafNode(None, None, None)
        # self.assertRaises(ValueError, node.to_html) # Alternative to current (using manager style)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_raw_text(self):
        node = LeafNode(None, "Raw Text String!?")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.to_html(), "Raw Text String!?")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode(
            "a",
            "Clickable Link!",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Clickable Link!</a>',
        )

    def test_inherited_repr(self):
        node = LeafNode(
            "p",
            "What a strange world",
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "LeafNode(p, What a strange world, {'class': 'primary'})",
        )

    ###     ParentNode    ####
    def test_parent_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        # self.assertRaises(ValueError, node.to_html) # Alternative to current (using manager style)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_children(self):
        node = ParentNode("b", None)
        # self.assertRaises(ValueError, node.to_html) # Alternative to current (using manager style)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_no_child_list(self):
        node = ParentNode("b", [])
        # self.assertRaises(ValueError, node.to_html) # Alternative to current (using manager style)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_with_many_descendants(self):
        great_grandchild_node = LeafNode("b", "great grandchild")
        grandchild_node = ParentNode("h1", [great_grandchild_node])
        parent_node = ParentNode(
            "div",
            [
                LeafNode("p", "child 1"),
                ParentNode("span", [grandchild_node]),
                LeafNode("b", "child 3"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>child 1</p><span><h1><b>great grandchild</b></h1></span><b>child 3</b></div>",
        )


if __name__ == "__main__":
    unittest.main()
