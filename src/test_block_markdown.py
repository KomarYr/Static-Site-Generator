import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_separations(self):
        pass


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




