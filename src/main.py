from textnode import TextNode, TextType
from htmlnode import LeafNode
from enum import Enum


    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    pass

def main():
    dummy = TextNode("Dummy text",TextType.BOLD)
    print (dummy)



main()