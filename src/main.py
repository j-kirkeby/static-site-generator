from textnode import *
from nodesplitter import *
import shutil
import os

def main():
    copy_static()
    generate_pages_recursive("content", "template.html", "public")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path.replace(".md", ".html"))
    else:
        dir = os.listdir(dir_path_content)
        for item in dir:
            generate_pages_recursive(f"{dir_path_content}/{item}", template_path, 
                          f"{dest_dir_path}/{item}")

def recurse_copy(path, dest_path):
    print(path, dest_path)
    if os.path.isfile(path):
        shutil.copy(path, dest_path)
    else:
        os.mkdir(dest_path)
        dir = os.listdir(path)
        for item in dir:
            recurse_copy(f"{path}/{item}", f"{dest_path}/{item}")

def copy_static():
    if os.path.exists("public"):
        shutil.rmtree("public")
    recurse_copy("static", "public")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path) as file: 
        markdown = file.read()
    
    template = ""
    with open(template_path) as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    directory = os.path.dirname(dest_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(page)


main()