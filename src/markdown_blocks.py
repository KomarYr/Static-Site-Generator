from enum import Enum
import re


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






if __name__ == "__main__":
    text = "```\nThis is code block.\n```"
    print(block_to_block_type(text))
