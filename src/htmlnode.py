

class HTMLNode():

    def __init__(self,tag = None,value = None,children = None,props = None):
        self.tag = tag #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #A list of HTMLNode objects representing the children of this node
        self.props = props #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError ("child classes method should override this")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        printed_string = ""
        for entry in self.props:
            printed_string += f' {entry}="{self.props[entry]}"'
        return printed_string

    def __repr__(self):
        print ("HTMLNODE:")
        print (f"tag = {self.tag}")
        print (f"value = {self.value}")
        if self.children != None:
            print (f"Has child HTMLNodes: {self.children}")
        if self.props != None:
            print (self.props_to_html())
        print ("")

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (self.tag == other.tag) and (self.value == other.value) and (self.children == other.children) and (self.props == other.props)
        raise NotImplementedError
        


class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.value == None:
            raise ValueError ("all leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        print ("HTMLNODE (LeafNode):")
        print (f"tag = {self.tag}")
        print (f"value = {self.value}")
        if self.children != None:
            print (f"Has child HTMLNodes: {self.children}")
        if self.props != None:
            print (self.props_to_html())
        print ("")

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None:
            raise ValueError ("all parent nodes must have a tag")
        if self.children == None or self.children == []:
            raise ValueError ("Parent node must have child nodes")
        to_html_string = (f"<{self.tag}{self.props_to_html()}>")
        for entry in self.children:
            to_html_string += entry.to_html()
        to_html_string += (f"</{self.tag}>")
        return to_html_string
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
