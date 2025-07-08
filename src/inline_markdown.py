from textnode import TextNode,TextType
from enum import Enum
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def convert_single_node_into_split_list(text_node,delimiter,text_type):
        if text_node.text_type != TextType.TEXT:
            return [text_node]
        split_text = text_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception (f"invalid markdown - found {delimiter} instance of delimiter")
    
        split_node = []
        for i in range(len(split_text)):
            if split_text[i] != "": #empty string handling
                if i % 2 == 0:
                    split_node.append(TextNode(split_text[i],TextType.TEXT,None))
                else:
                    split_node.append(TextNode(split_text[i],text_type,None))
        
        return split_node
    
    new_nodes = []
    for entry in old_nodes:
        new_nodes.extend(convert_single_node_into_split_list(entry,delimiter,text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_single_node_img_or_link(old_node, type):
    new_nodes = []
    if type == TextType.IMAGE:
        tuples = extract_markdown_images(old_node.text)
        
    elif type == TextType.LINK:
        tuples = extract_markdown_links(old_node.text)
        
    else:
        raise ValueError ('type should be either TextType.IMAGE or TextType.LINK')
    
    current = old_node.text
    for entry in tuples:
        alt = entry[0]
        link = entry[1]
        pattern = ""
        if type == TextType.IMAGE:
            pattern += "!"
        pattern += (f"[{alt}]({link})")
        current_split = current.split(pattern,1)
        if current_split[0] != "":
            new_nodes.append (TextNode(current_split[0],TextType.TEXT,None))
        new_nodes.append (TextNode(alt,type,link))
        current = (current_split[-1])
    if current != "":
        new_nodes.append (TextNode(current,TextType.TEXT,None))
    return new_nodes
           

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_single_node_img_or_link(node,TextType.IMAGE))
        else:
            new_nodes.extend([node])
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_single_node_img_or_link(node,TextType.LINK))
        else:
            new_nodes.extend([node])
    return new_nodes


def text_to_textnodes_sample(text):
    #im just going to go ahead and say, this does everything in one line. why? beacuse I don't see the need to add a variable for every step. 
    #if you want this to be readable, use the principles of functional programming to unwrap it. that's how I built this too :)
    start_node = (TextNode(text,TextType.TEXT,None))
    a = split_nodes_image([start_node])
    b = split_nodes_link(a)
    c = split_nodes_delimiter(b,"**",TextType.BOLD)
    d = split_nodes_delimiter(c,"*",TextType.ITALIC)
    e = split_nodes_delimiter(d,"_",TextType.ITALIC)
    return split_nodes_delimiter(e,"`",TextType.CODE)

def text_to_textnodes(text):
    #im just going to go ahead and say, this does everything in one line. why? beacuse I don't see the need to add a variable for every step. 
    #if you want this to be readable, use the principles of functional programming to unwrap it. that's how I built this too :)
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_link(split_nodes_image([(TextNode(text,TextType.TEXT,None))])),"**",TextType.BOLD),"*",TextType.ITALIC),"_",TextType.ITALIC),"`",TextType.CODE)


#print (text_to_textnodes(r"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))