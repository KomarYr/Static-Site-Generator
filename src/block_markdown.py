def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")
    text = []
    for line in lines:
        if line == "":
            continue
        text.append(line.strip())
    return text






if __name__ == "__main__":
    md = """
This is **bolded** paragraph

This is another aparagraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    print(markdown_to_blocks(md))
