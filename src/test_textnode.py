import unittest

from textnode import TextNode, TextType
from htmlnode import *


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

if __name__ == "__main__":
    unittest.main()