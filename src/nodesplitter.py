from textnode import *
from htmlnode import *
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
