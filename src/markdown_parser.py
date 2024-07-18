from textnode import TextNode
from htmlnode import LeafNode, ParentNode
import re

markdown_types = {
    "*":"italics",
    "**":"bold",
    "`":"code",
}

def split_nodes_delimiter(old_nodes, delimiter):
    placeholder = "!PLACEHOLDER!"
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text": new_nodes.append(node)
        else:
            node_text = node.text
            if delimiter == "*": node_text = node_text.replace("**", placeholder)
            split_nodes = node_text.split(delimiter)
            if len(split_nodes) == 1: new_nodes.append(node)
            elif len(split_nodes) % 2 == 0:
                raise Exception(f"Invalid Markdown Syntax Found in node: {node}")
            else:
                for i, node_split in enumerate(split_nodes):
                    if i % 2 != 0:
                        new_nodes.append(TextNode(text = node_split.replace(placeholder, "**"), text_type = markdown_types[delimiter]))
                    elif node_split != "":
                        new_nodes.append(TextNode(text = node_split.replace(placeholder, "**"), text_type = "text"))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_links_images(old_nodes, find_images):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        found = extract_markdown_images(current_text) if find_images else extract_markdown_links(current_text)
        if len(found) == 0:
            new_nodes.append(node)
            continue
        for found_item in found:
            search_string = ("!" if find_images else "") + f"[{found_item[0]}]({found_item[1]})"
            sections = current_text.split(search_string, 1)
            if sections[0] != "": new_nodes.append(TextNode(text_type="text", text=sections[0]))
            text_type = "image" if find_images else "link"
            new_nodes.append(TextNode(text_type=text_type, text=found_item[0], url = found_item[1]))
            current_text = sections[1]
        if current_text != "": new_nodes.append(TextNode(text= current_text, text_type="text"))
    return new_nodes

def text_to_text_nodes(text):
    current_parse = [TextNode(text=text, text_type="text")]
    for type in markdown_types:
        current_parse = split_nodes_delimiter(current_parse, type)
    current_parse = split_nodes_links_images(current_parse, True)
    current_parse = split_nodes_links_images(current_parse, False)
    return current_parse

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    cleaned_list = list(map(lambda x: x.strip(), split_markdown))
    return list(filter(lambda x: x != "", cleaned_list))

def block_to_block_type(block):
    split_by_lines = block.split("\n")
    if len(split_by_lines) == len(list(filter(lambda x: len(x) > 1 and x[0] == '>' and x[1] == ' ', split_by_lines))): return "quote"
    if len(split_by_lines) == len(list(filter(lambda x: len(x) > 1 and (x[0] == '*' or x[0] == '-') and x[1] == ' ', split_by_lines))): return "unordered_list"
    if len(split_by_lines) == len(list(filter(lambda x: len(x.split('.')) > 0 and x.split('.')[0].isdigit(), split_by_lines))): return "ordered_list"
    split_by_space = block.split(" ")
    if len(split_by_space) > 0 and len(split_by_space[0]) <= 6 and all(c == '#' for c in split_by_space[0]): return "heading"
    if len(block) > 6 and block[0:3] == "```" and block[-3:] == "```": return "code"
    return "paragraph"

def create_node_blocks_from_string(text, tag):
    text_nodes = text_to_text_nodes(text)
    leaf_nodes = list(map(lambda x: x.to_html_node(), text_nodes))
    return ParentNode(tag = tag, children = leaf_nodes)
    
def create_node_blocks_from_list(str_list, child_tag, parent_tag):
    sub_blocks = []
    for str in str_list:
        sub_blocks.append(create_node_blocks_from_string(str, child_tag))
    return ParentNode(tag = parent_tag, children = sub_blocks)

def convert_quote_block(block):
    if block_to_block_type(block) != "quote":
        raise Exception("Attempting to convert non-quote block to a quote")
    split_by_lines = block.split("\n")
    cleaned = "\n".join(list(map(lambda x: x[2:], split_by_lines)))
    return create_node_blocks_from_string(cleaned, "blockquote")

def convert_heading_block(block):
    if block_to_block_type(block) != "heading":
        raise Exception("Attempting to convert non heading block to a heading")
    split_by_first_space = block.split(" ",1)
    h_tag = f"h{len(split_by_first_space[0])}"
    return create_node_blocks_from_string(split_by_first_space[1], h_tag)

def convert_code_block(block):
    if block_to_block_type(block) != "code":
        raise Exception("Attempting to convert non code block to a code block")
    cleaned = block[3:-3]
    code_node = create_node_blocks_from_string(cleaned, "code")
    return ParentNode(tag = "pre", children=[code_node])

def convert_paragraph_block(block):
    if block_to_block_type(block) != "paragraph":
        raise Exception("Attempting to convert non-paragraph block to paragraph block")
    return create_node_blocks_from_string(block, "p")

def convert_list_block(block):
    block_type = block_to_block_type(block)
    if block_type != "ordered_list" and block_type != "unordered_list":
        raise Exception("Attempting to convert non-list block to list block")
    tag = "ul" if block_type == "unordered_list" else "ol"
    split_by_lines = block.split("\n")
    remove_leading_list = list(map(lambda x: x.split(" ",1)[1], split_by_lines))
    return create_node_blocks_from_list(remove_leading_list, "li", tag)

def convert_block(block):
    match block_to_block_type(block):
        case "heading":
            return convert_heading_block(block)
        case "code":
            return convert_code_block(block)
        case "quote":
            return convert_quote_block(block)
        case "unordered_list" | "ordered_list":
            return convert_list_block(block)
        case "paragraph":
            return convert_paragraph_block(block)

def convert_markdown(text):
    blocks = markdown_to_blocks(text)
    converted_blocks = list(map(lambda x: convert_block(x), blocks))
    return ParentNode(tag = "div", children = converted_blocks)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == "heading":
            converted_block = convert_heading_block(block)
            if converted_block.tag == "h1":
                return converted_block.children[0].value
    raise Exception("H1 heading not found in document, and required for parse")

def main():
    pass

main()
