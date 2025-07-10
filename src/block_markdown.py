from enum import Enum
from htmlnode import HTMLNode,LeafNode,ParentNode
from textnode import TextNode, TextType,text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(string):
    def determine_pattern(string,block_type):
        #code
        if block_type == BlockType.CODE:
            return string.startswith("```") and string.endswith("```")
        if block_type == BlockType.HEADING:
            n = ["# ","## ","### ","#### ","##### ","###### "]
            for entry in n:
                if  string.startswith(entry):
                    return True
            return False
        if block_type == BlockType.QUOTE:
            n = string.split("\n")
            for entry in n:
                if not entry.startswith(">"):
                    return False
        if block_type == BlockType.UNORDERED_LIST:
            n = string.split("\n")
            for entry in n:
                if not entry.startswith("- "):
                    return False
        if block_type == BlockType.ORDERED_LIST:
            n = string.split("\n")
            for i in range (1, len(n) + 1):
                if not n[i-1].startswith(f"{i}. "):
                    return False
        return True
    
    if determine_pattern(string,BlockType.CODE):
        return BlockType.CODE
    if determine_pattern(string,BlockType.HEADING):
        return BlockType.HEADING
    if determine_pattern(string,BlockType.QUOTE):
        return BlockType.QUOTE
    if determine_pattern(string,BlockType.UNORDERED_LIST):
        return BlockType.UNORDERED_LIST
    if determine_pattern(string,BlockType.ORDERED_LIST):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
def markdown_to_blocks(input_string):
    a = input_string.split("\n\n")
    b = list(filter(lambda n: n != "", a))
    c = list(map(lambda n: n.strip(),b))
    d = list(filter(lambda n: n != "", c))
    return d

def markdown_to_html_node(markdown):

    def determine_heading_tag(block): #only used if the block is a heading
        i = 1
        for entry in ["# ","## ","### ","#### ","##### ","###### "]:
            if block.startswith(entry):
                return (f"h{i}")
            i += 1
        raise Exception ("incompatible markdown - block is not a heading yet was passed with a heading BlockType")

    def block_to_parent_node(block,type): #convery a single block into a parent node, which will contain children depending on it's type.
        def get_block_top_html_tag(type):
            if type == BlockType.CODE:
                return "pre"
            if type == BlockType.QUOTE:
                return "blockquote"
            if type == BlockType.ORDERED_LIST:
                return "ol"
            if type == BlockType.UNORDERED_LIST:
                return "ul"
            if type == BlockType.HEADING:
                return determine_heading_tag(block)
            if type == BlockType.PARAGRAPH:
                return "p"
            
        def text_to_children(block,type):
            if type == BlockType.CODE:
                raw_string = block.strip("`").lstrip("\n") #newline handling slice
                child_node = TextNode(raw_string,TextType.CODE)
                return [text_node_to_html_node(child_node)]
            
            child_nodes = []

            if type == BlockType.PARAGRAPH:
                raw_string = block.replace("\n"," ")
                return list(map(lambda n: text_node_to_html_node(n),text_to_textnodes(raw_string)))
            
            if type == BlockType.QUOTE:
                raw_string = block[1:].replace("\n"," ").replace(">","").strip()
                return list(map(lambda n: text_node_to_html_node(n),text_to_textnodes(raw_string)))
            
            if type == BlockType.HEADING:
                heading_to_slice = 1 + int(determine_heading_tag(block)[1]) #this will give the number of '#' characters in the heading. adding 1 to it because there's a space.
                raw_string = block[heading_to_slice:].replace("\n"," ")
                return list(map(lambda n: text_node_to_html_node(n),text_to_textnodes(raw_string)))
            
            if type == BlockType.UNORDERED_LIST:
                raw_markdown_list = block.split("\n")
                markdown_list = list(map(lambda n: n[2:],raw_markdown_list)) #this slices all the markdown off of the list items
                
                for entry in markdown_list:
                    #grandchild_nodes = text_to_textnodes(entry)
                    grandchild_nodes = list(map(lambda n: text_node_to_html_node(n),text_to_textnodes(entry)))
                    child_nodes.append(ParentNode("li",grandchild_nodes))
                return child_nodes
            
            if type == BlockType.ORDERED_LIST:
                raw_markdown_list = block.split("\n")
                markdown_list = list(map(lambda n: n[3:],raw_markdown_list)) #this slices all the markdown off of the list items
                
                for entry in markdown_list:
                    grandchild_nodes = list(map(lambda n: text_node_to_html_node(n),text_to_textnodes(entry)))
                    child_nodes.append(ParentNode("li",grandchild_nodes))
                return child_nodes
        
        return ParentNode(get_block_top_html_tag(type), text_to_children(block,type))

    list_of_blocks = markdown_to_blocks(markdown)
    children = []
    for entry in list_of_blocks:
        entry_type = block_to_block_type(entry)
        children.append(block_to_parent_node(entry,entry_type))

    return ParentNode("div",children,None)

def extract_title(markdown_doc):
    block_list = markdown_to_blocks(markdown_doc)
    for entry in block_list:
        if entry.strip().startswith("# "):
            return entry.strip()[2:].strip()
    raise Exception ("Missing h1 header in argument - markdown_doc")