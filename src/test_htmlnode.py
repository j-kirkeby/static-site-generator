import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
    
    def test_print(self):
        node1 = HTMLNode()
        self.assertEqual(str(node1), "HTMLNode(None, None, None, None)")
        node2 = HTMLNode("p", "hei", None, {"style": "color:red"})
        self.assertEqual(str(node2), "HTMLNode(p, hei, None, {'style': 'color:red'})")
    
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com",
            "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    # Leaf nodes
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "See this link", props={"href":"link.com"})
        self.assertEqual(node.to_html(), '<a href="link.com">See this link</a>')
    
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Title", props={"style":"color:red"})
        self.assertEqual(node.to_html(), '<h1 style="color:red">Title</h1>')

    # Parent nodes
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_tml_with_many_children(self):
        grandchild_node = LeafNode("b","bold strategy")
        child_node1 = ParentNode("p", [grandchild_node])
        child_node2 = LeafNode("a", "See this link", props={"href":"link.com"})
        parent_node = ParentNode("main", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            '<main><p><b>bold strategy</b></p><a href="link.com">See this link</a></main>'
        )

if __name__ == "__main__":
    unittest.main()