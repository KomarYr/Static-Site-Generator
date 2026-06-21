from textnode import TextNode, TextType
from copy_content import copy_content


def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    #print(text_node)
    source_directory = "./static"
    destination_directory = "./public"
    copy_content(source_directory, destination_directory)



main()
