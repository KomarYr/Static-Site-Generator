import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    
    def test_not_eq(self):
        node = TextNode("Not equal test cases", TextType.ITALIC)
        node2 = TextNode("Not equal test cases", TextType.BOLD)
        self.assertNotEqual(node, node2)

    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)
    

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)
            

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
                "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
            )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {'href': 'https://www.boot.dev'})


class TestSplitNodesDelimeter(unittest.TestCase):
    def test_text_with_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
                new_nodes,
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                ]
        )
    
    def test_text_with_bold_text(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
                new_nodes,
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded phrase", TextType.BOLD),
                    TextNode(" in the middle", TextType.TEXT),
                ]
        )

    def test_text_with_italic_text(self):
        node = TextNode("This is an _italic_ word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
                new_nodes,
                [
                    TextNode("This is an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word.", TextType.TEXT)
                ]
        )











if __name__ == "__main__":
    unittest.main()
