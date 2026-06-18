import unittest
from textnode import TextNode, TextType
from inline_markdown import (
        text_to_textnodes,
        split_nodes_delimiter,
        split_nodes_image, 
        split_nodes_link,
        extract_markdown_images, 
        extract_markdown_links
)

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


class TestImageUrl(unittest.TestCase):
    def test_extraction(self):
         text = """
            This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) 
            and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)
        """
         self.assertEqual(
                 extract_markdown_images(text),
                 [
                     ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
                     ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
                 ]
        )

    def test_empty_text_extraction(self):
        text = ""
        self.assertEqual(extract_markdown_images(text), [])

    
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )
    

    def test_split_with_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",    
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )


    def test_split_image_with_text_after_and_before(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) surronded by text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" surronded by text.", TextType.TEXT)
            ],
            new_nodes
        )



class TestLinkUrl(unittest.TestCase):
    def text_extraction(self):
        text = """
            This is text with a link [to boot dev](https://www.boot.dev) 
            and [to youtube](https://www.youtube.com/@bootdotdev)
        """
        self.assertEqual(
                extract_markdown_links(text),
                [
                    ("to boot dev", "https://www.boot.dev"), 
                    ("to youtube", "https://www.youtube.com/@bootdotdev")
                ]
        )
    
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
            ],
            new_nodes
        )


    def test_split_link_with_text_after_and_before(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) click me.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" click me.", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_links_at_start(self):
        node = TextNode(
            "[boot dev](https://www.boot.dev) is great",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is great", TextType.TEXT),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_with_all_elements(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
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
            ],
            new_nodes
        )











