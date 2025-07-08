import unittest

from textnode import TextNode, TextType,text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.LINK,"https://www.twitch.tv/directory/following")
        node2 = TextNode("This is a text node", TextType.LINK,"https://www.twitch.tv/directory/following")
        self.assertEqual(node, node2)

    def test_noneq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noneq_link(self):
        node = TextNode("This is a text node", TextType.LINK,"https://www.twitch.tv/directory/following")
        node2 = TextNode("This is a text node", TextType.LINK,"https://www.youtube.com/")
        self.assertNotEqual(node, node2)

    def test_noneq_link_nourl(self):
        node = TextNode("This is a text node", TextType.LINK,"https://www.twitch.tv/directory/following")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")




if __name__ == "__main__":
    unittest.main()