from htmlnode import LeafNode
from textnode import TextNode
from markdown_parser import extract_title, convert_markdown
import os
import shutil

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value = text_node.text)
        case "bold":
            return LeafNode(tag = "b", value = text_node.text)
        case "italic":
            return LeafNode(tag = "i", value = text_node.text)
        case "code":
            return LeafNode(tag = "code", value = text_node.text)
        case "link":
            return LeafNode(tag = "a", value = text_node.text, props = {"href": text_node.url}) 
        case "image":
            return LeafNode(tag= "img", value = "", props = {"src": text_node.url, "alt" : text_node.text}) 
        case _:
            raise Exception("Attempted to provide a text_node type not recognized by html conversion.")

def copy_dir(source_path, target_path):
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)
    file_paths = os.listdir(source_path)
    for path in file_paths:
        new_source = os.path.join(source_path, path)
        if os.path.isdir(new_source):
            new_target = os.path.join(target_path, path)
            copy_dir(new_source, new_target)
        else:
            shutil.copy(new_source, target_path)

def get_project_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '..'))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    html = ""

    with open(from_path, 'r') as file:
        markdown = file.read()
    page_title = extract_title(markdown)
    page_content = convert_markdown(markdown).to_html()

    with open(template_path, 'r') as template_file:
        template = template_file.read()
        html = template.replace("{{ Title }}", page_title).replace("{{ Content }}", page_content)
    
    with open(dest_path, 'w') as new_file:
        new_file.write(html)

def generate_pages(root_path, template_path, dest_path):
    file_paths = os.listdir(root_path)
    for path in file_paths:
        full_source_path = os.path.join(root_path, path)
        full_target_path = os.path.join(dest_path, path)
        if os.path.exists(full_target_path): shutil.rmtree(full_target_path)
        if os.path.isdir(full_source_path): 
            os.mkdir(full_target_path)
            generate_pages(full_source_path, template_path, full_target_path)
        else:
            html_target_path = os.path.splitext(full_target_path)[0] + '.html'
            generate_page(full_source_path, template_path, html_target_path)
    

def main():
    project_path = get_project_path()
    static_path = os.path.join(project_path, 'static')
    public_path = os.path.join(project_path, 'public')
    content_path = os.path.join(project_path, 'content')
    template_path = os.path.join(project_path, 'template.html')
    copy_dir(static_path, public_path)
    generate_pages(content_path, template_path, public_path)



main()
