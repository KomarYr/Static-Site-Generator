import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_tag_empty(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())
        self.assertEqual(
                "HTMLNode(None, None, None, None)", repr(node))


    def test_without_value(self):
        node = HTMLNode(tag="p", children=HTMLNode())
        self.assertIsNone(node.value)
        self.assertIsInstance(node.children, HTMLNode)

    def test_without_children(self):
        node = HTMLNode(tag="div", value="hello")
        self.assertIsNone(node.children)
        self.assertIsNotNone(node.value)



if __name__ == "__main__":
    unittest.main()
