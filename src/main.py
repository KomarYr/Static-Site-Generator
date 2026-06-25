import sys
from textnode import TextNode, TextType
from copy_content import copy_content
from generate_page import generate_page_recursive


static_directory = "./static"
content_directory = "./content"
destination_directory = "./docs"
template_path = "./template.html"


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Copying static files to public directory...")
    copy_content(static_directory, destination_directory)

    print("Generating content...")
    generate_page_recursive(content_directory, template_path, basepath)


main()
