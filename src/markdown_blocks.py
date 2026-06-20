import re
from enum import Enum
from htmlnode import ParentNode, HTMLNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list" 


def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")
    text = []
    for line in lines:
        if line == "":
            continue
        text.append(line.strip())
    return text


def block_to_block_type(text: str) -> BlockType:
    lines = text.split("\n")
    if re.match(r"^#{1,6} ", text):
        return BlockType.HEADING
    elif re.match(r"^```\n[\s\S]*```$", text):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    elif text.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_node = block_to_html_node(block)
        block_nodes.append(html_node)
    return ParentNode("div", block_nodes, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.QUOTE:
            return to_blockquote(block)
        case BlockType.HEADING:
            return to_heading(block)
        case BlockType.ULIST:
            return to_unordered_list(block)
        case BlockType.OLIST:
            return to_ordered_list(block)
        case BlockType.CODE:
            return to_code(block)
        case BlockType.PARAGRAPH:
            return to_paragraph(block)
        case _:
            raise ValueError("invalid block type")


def text_to_children(text: str) -> list[HTMLNode]:
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def to_code(block: str) -> ParentNode:
    code_text = block.replace("```", "")    # block[4:-3]
    text_node = TextNode(code_text.lstrip(), TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [html_node])


def to_blockquote(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def to_heading(block: str) -> ParentNode:
    h_level, txt = block.split(" ", 1)
    heading_tag = f"h{len(h_level)}"
    children = text_to_children(txt)
    return ParentNode(heading_tag, children)


def to_unordered_list(block: str) -> ParentNode:
    li_nodes = []
    lines = block.split("\n")
    for line in lines:
        child = text_to_children(line.replace("- ", "", 1))
        li_node = ParentNode("li", child)
        li_nodes.append(li_node)
    return ParentNode("ul", li_nodes)


def to_ordered_list(block: str) -> ParentNode:
    li_nodes = []
    items = block.split("\n")
    for i, item in enumerate(items, 1):
        child = text_to_children(item.replace(f"{i}. ", "", 1))
        li_node = ParentNode("li", child)
        li_nodes.append(li_node)
    return ParentNode("ol", li_nodes)


def to_paragraph(block: str) -> ParentNode:
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)










if __name__ == "__main__":
    text = "## Heading text here\n\n> This is quotes first line\n> And second line\n\n- Firsth item\n- Second item\n\n```\nThis is code block\n```"
    #text = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
    node = markdown_to_html_node(text)
    print(node.to_html())
