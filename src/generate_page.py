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
            generate_page(current_path, template_path, (dst / item).with_suffix(".html"))
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
    template.replace("{{ Title }}", title)
    template.replace("{{ Content }}", content)
    template.replace('href="/', f'href="{dest_path}')
    template.replace('srs="/', f'srs="{dest_path}')

    if not os.path.dirname(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    with open(dest_path, "w") as dst:
        dst.write(template)





if __name__ == "__main__":
    pass
