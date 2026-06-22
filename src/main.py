from textnode import TextNode, TextType
from copy_content import copy_content
from generate_page import generate_page


source_directory = "./static"
destination_directory = "./public"


def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    #print(text_node)
    copy_content(source_directory, destination_directory)
    generate_page("./content/index.md", "./template.html", "public/index.html")


main()
