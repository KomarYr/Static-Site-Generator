from textnode import TextNode, TextType
from copy_content import copy_content
from generate_page import generate_page_recursive


static_directory = "./static"
content_directory = "./content"
destination_directory = "./public"
template_path = "./template.html"


def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    #print(text_node)
    copy_content(static_directory, destination_directory)
    generate_page_recursive(content_directory, template_path, destination_directory)


main()
