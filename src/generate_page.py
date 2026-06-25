import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node



def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    src = Path(dir_path_content)
    dst = Path(dest_dir_path)
    print(f"sourse: {src}, destination: {dst}")
    if not src.exists():
        raise ValueError(f"{dir_path_content} is not exists")
    for item in os.listdir(src):
        current_path = src / item   # forward slash is like join
        if current_path.is_file():
            dst.mkdir(parents=True, exist_ok=True)
            generate_page(current_path, template_path, (dst / item).with_suffix(".html")
            continue
        new_dst = dst / item
        generate_page_recursive(current_path, template_path, new_dst)



def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("Wrong Markdown file, missing header h1")



def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        md = file.read()
    node = markdown_to_html_node(md)
    content = node.to_html()
    title = extract_title(md)
    with open(template_path) as file:
        template = file.read()
    lines = template.split("\n")
    new_page = ""
    title_placeholder = "{{ Title }}"
    content_placeholder = "{{ Content }}"
    for line in lines:
        if title_placeholder in line:
            line = line.replace("{{ Title }}", title)
        if content_placeholder in line:
            line = line.replace("{{ Content }}", content)
        new_page += line
    #print(new_page)
    #if not os.path.dirname(dest_path):
        #os.mkdir(dest_path)
    with open(dest_path, "w") as dst:
        dst.write(new_page)





if __name__ == "__main__":
    pass
