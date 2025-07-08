from enum import Enum
from htmlnode import LeafNode

class TextType(Enum): #these used to be called something else, but i matched them to the solution files for easier translation moving forward.
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():

    def __init__(self,content,type,url = None):
        self.text = content
        self.text_type = type
        self.url = url

    def __eq__(self, other):
        return ((self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url))
    
    def __repr__(self):
        if self.url == None:
            return (f"TextNode({self.text}, {self.text_type})")
        return (f"TextNode({self.text}, {self.text_type}, {self.url})")
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("a", text_node.text,None,{"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", None, {"src" : text_node.url, "alt": text_node.text})
    raise ValueError(f"can't convert invalid textnode: {text_node.text_type}")