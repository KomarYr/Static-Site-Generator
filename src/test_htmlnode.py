import unittest
from htmlnode import HTMLNode, LeafNode


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


if __name__ == "__main__":
    unittest.main()
