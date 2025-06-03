from textnode import *
from htmlnode import *
from blocktype import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split = node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise Exception(f"Missing closing delimiter: {delimiter}")
        
        special_node = False
        for text in split:
            if text and special_node:
                new_nodes.append(TextNode(text, text_type))
            elif text and not special_node:
                new_nodes.append(TextNode(text, TextType.TEXT))

            if special_node:
                special_node = False
            else:
                special_node = True

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        
        rest = node.text
        for i in images:
            parts = rest.split(f"![{i[0]}]({i[1]})")
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(i[0], TextType.IMAGE, i[1]))
            rest = parts[1]  
        if rest:
            new_nodes.append(TextNode(rest, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)

        rest = node.text
        for i in links:
            parts = rest.split(f"[{i[0]}]({i[1]})")
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(i[0], TextType.LINK, i[1]))
            rest = parts[1]  
        if rest:
            new_nodes.append(TextNode(rest, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes) # Extract images
    nodes = split_nodes_link(nodes) # Extract links
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE) # Extract codes
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD) # Extract bold
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) # Extract italic
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)-1, -1, -1):
        blocks[i] = blocks[i].strip()
        if len(blocks[i]) == 0:
            blocks.remove(blocks[i])
    return blocks

def paragraph_to_html(block):
    text_nodes = text_to_textnodes(block)
    children = []
    for node in text_nodes:
        children.append(TextNode.text_node_to_html_node(node))
    return ParentNode("p", children)

def heading_to_html(block):
    # Splits into parts[0]="#...", parts[1]=text
    parts = block.split(" ", 1)
    length = len(parts[0])
    tag = f"h{length}"
    children = []
    text_nodes = text_to_textnodes(parts[1])
    for node in text_nodes:
        children.append(TextNode.text_node_to_html_node(node))
    return ParentNode(tag, children)

def code_to_html(block):
    # remove code 
    text = block[3:-3].strip()
    children = [TextNode.text_node_to_html_node(TextNode(text, TextType.TEXT))]
    return ParentNode("pre", [ParentNode("code", children)])

def quote_to_html(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line[2:] # remove "> "
        nodes = text_to_textnodes(text)
        for node in nodes:
            children.append(TextNode.text_node_to_html_node(node))
    return ParentNode("blockquote", children)

def ul_to_html(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line[2:] # remove "- "
        nodes = text_to_textnodes(text)
        li_children = []
        for node in nodes:
            li_children.append(TextNode.text_node_to_html_node(node))
        children.append(ParentNode("li", li_children))
    return ParentNode("ul", children)

def ol_to_html(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        text = line.split(" ", 1)[1] # remove the number, i.e. "1. " or "20. "
        nodes = text_to_textnodes(text)
        li_children = []
        for node in nodes:
            li_children.append(TextNode.text_node_to_html_node(node))
        children.append(ParentNode("li", li_children))
    return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        type = BlockType.block_to_block_type(block)
        match type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html(block))
            case BlockType.HEADING:
                children.append(heading_to_html(block))
            case BlockType.CODE:
                children.append(code_to_html(block))
            case BlockType.QUOTE:
                children.append(quote_to_html(block))
            case BlockType.UNORDERED_LIST:
                children.append(ul_to_html(block))
            case BlockType.ORDERED_LIST:
                children.append(ol_to_html(block))
    
    html = ParentNode("div", children)
    return html

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[:2] == "# ":
            return line[2:]
    raise Exception("No title in markdown")


