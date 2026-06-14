import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_tag_empty(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())
        self.assertEqual(
                "HTMLNode(None, None, children: None, None)", repr(node))


    def test_without_value(self):
        node = HTMLNode(tag="p", children=HTMLNode())
        self.assertIsNone(node.value)
        self.assertIsInstance(node.children, HTMLNode)


    def test_without_children(self):
        node = HTMLNode(tag="div", value="hello")
        self.assertIsNone(node.children)
        self.assertIsNotNone(node.value)


    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_leaf_invalid_value(self):
        node = LeafNode("p", None)
        # Call .to_html() only inside with block
        with self.assertRaises(ValueError) as msg:
            node.to_html()
            
        self.assertEqual(str(msg.exception), "leaf nodes must have a value")
        
    def test_leaf_empty_tag(self):
        node = LeafNode(None, "only raw text")
        self.assertEqual(node.to_html(), "only raw text")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_link(self):
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("span", [child_node])
        node = ParentNode(
            "div",
            [
                parent_node,
                LeafNode("i", "italic text")
            ]
        )
        self.assertEqual(node.to_html(), '<div><span><a href="https://www.google.com">Click me!</a></span><i>italic text</i></div>')



if __name__ == "__main__":
    unittest.main()
