import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_basic_eq(self):
        node = HTMLNode("p","H",None,{"target": "_blank"})
        node2 = HTMLNode("p","H",None,{"target": "_blank"})
        self.assertEqual(node, node2)

    def test_basic_noneq_01(self):
        node = HTMLNode("p","H",None,{"target": "_blank"})
        node2 = HTMLNode("p","L",None,{"target": "_blank"})
        self.assertNotEqual(node, node2)

    def test_basic_noneq_02(self):
        node = HTMLNode("p","H",None,{"target": "_blank"})
        node2 = HTMLNode("p","H",None,{"target": "_blak"})
        self.assertNotEqual(node, node2)

    def test_basic_noneq_03(self):
        node = HTMLNode(None,"H",None,{"target": "_blank"})
        node2 = HTMLNode("p","H",None,{"target": "_blank"})
        self.assertNotEqual(node, node2)

    def test_basic_noneq_04(self):
        node = HTMLNode("p")
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)

    def test_force_error_if_constant(self):
        node = HTMLNode("p","H",None,{"target": "_blank"})
        node2 = HTMLNode("p","H",None,{"target": "_blank"})
        force_error = False
        if force_error:
            node2.tag = "a"
        self.assertEqual(node, node2)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!",None,{"href": "https://www.google.com"})
        self.assertEqual(node.to_html() , '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )



if __name__ == "__main__":
    unittest.main()