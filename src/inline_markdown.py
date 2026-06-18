import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: list[TextNode], 
        delimiter: str, 
        text_type: TextType
    ) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        splited_text = old_node.text.split(delimiter)
        if len(splited_text) % 2 == 0:
            raise Exception("Closing delimiter is not found, that's invalid Markdown syntax")
        
        for i in range(len(splited_text)):
            if splited_text[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(splited_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(splited_text[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        extracted_images = extract_markdown_images(original_text)
        
        if not extracted_images:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        for image_alt, image_link in extracted_images:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            current_section = sections[0]
            if current_section != "":
                split_nodes.append(TextNode(current_section, TextType.TEXT))
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[-1]
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes            


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        extracted_links = extract_markdown_links(original_text)
        
        split_nodes = []
        if not extracted_links:
            new_nodes.append(old_node)
            continue
        for link_alt, link in extracted_links:
            sections = original_text.split(f"[{link_alt}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            current_section = sections[0]
            if current_section != "":
                split_nodes.append(TextNode(current_section, TextType.TEXT))
            split_nodes.append(TextNode(link_alt, TextType.LINK, link))
            original_text = sections[-1]
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes







if __name__ == "__main__":
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))
