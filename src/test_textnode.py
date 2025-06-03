import unittest

from textnode import TextNode, TextType
from htmlnode import *
from nodesplitter import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq_titles(self):
        node1 = TextNode("node1", TextType.ITALIC)
        node2 = TextNode("node2", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    
    def test_neq_types(self):
        node1 = TextNode("node", TextType.ITALIC)
        node2 = TextNode("node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_neq_urls1(self):
        node1 = TextNode("node", TextType.ITALIC, "www.hi.com")
        node2 = TextNode("node", TextType.ITALIC, "www.bye.com")
        self.assertNotEqual(node1, node2)

    def test_neq_urls2(self):
        node1 = TextNode("node", TextType.ITALIC, None)
        node2 = TextNode("node", TextType.ITALIC, "www.bye.com")
        self.assertNotEqual(node1, node2)
    
    def test_eq_urls(self):
        node1 = TextNode("node", TextType.ITALIC, None)
        node2 = TextNode("node", TextType.ITALIC)
        self.assertEqual(node1, node2)
    
    # text_node_to_html(text_node)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.link.com")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.link.com"})
    
    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "img/cat.jpg")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "img/cat.jpg", "alt": "This is an image node"})

    # Nodesplitter
    def test_nodesplitter_code(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            str(new_nodes),
            "[TextNode(This is a text with a , text, None), " \
            "TextNode(code block, code, None), " \
            "TextNode( word, text, None)]"
        )
    
    def test_nodesplitter_codes(self):
        node = TextNode("`This` is a text with a `code block` `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            str(new_nodes),
            "[TextNode(This, code, None), " \
            "TextNode( is a text with a , text, None), " \
            "TextNode(code block, code, None), " \
            "TextNode( , text, None), " \
            "TextNode(word, code, None)]"
        )
    
    def test_nodesplitter_fail(self):
        node = TextNode("This is missing a `closing delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_nodesplitter_bold(self):
        node = TextNode("This is a text with a *bold* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(
            str(new_nodes),
            "[TextNode(This is a text with a , text, None), " \
            "TextNode(bold, bold, None), " \
            "TextNode( word, text, None)]"
        )
    
    def test_nodesplitter_italic(self):
        node = TextNode("This is a text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            str(new_nodes),
            "[TextNode(This is a text with an , text, None), " \
            "TextNode(italic, italic, None), " \
            "TextNode( word, text, None)]"
        )
    
    # nodesplitter.py - extract functions
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)" \
            " ![image2](img/cat.jpg)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image2", "img/cat.jpg") ], matches
        )

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a [link text](link.com)"
        )
        self.assertListEqual([("link text", "link.com")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link text](link.com)" \
            "and a [link but different](url)"
        )
        self.assertListEqual(
            [("link text", "link.com"), ("link but different", "url")], matches
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word " \
        "and a `code block` and an " \
        "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a " \
        "[link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    # Node splitter : Markdown to blocks
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_whitespace(self):
        md = """
This is **bolded** paragraph with trailing whitespace


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line followed by four newlines



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph with trailing whitespace",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line followed by four newlines",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()