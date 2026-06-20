import unittest
from markdown_blocks import (
        markdown_to_blocks, 
        block_to_block_type, 
        markdown_to_html_node,
        BlockType
        )

class TestMarkdownToBlocks(unittest.TestCase):
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
                ],
            )

       
class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_types_multiple_lines(self):
        block = "> This is a quote.\nBut this line is normal text inside the same block!"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. This is firsth line of Oredered List.\n3. This second with wrong list number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```code without new line```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "- This is Unordered List\nThis is normal text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
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

    def test_codeblock(self):
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


    def test_mixins(self):
        md = "## Heading text here\n\n> This is quotes first line\n> And second line\n\n- Firsth item\n- Second item\n\n```\nThis is code block\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading text here</h2><blockquote>This is quotes first line And second line</blockquote><ul><li>Firsth item</li><li>Second item</li></ul><pre><code>This is code block\n</code></pre></div>",
        )




