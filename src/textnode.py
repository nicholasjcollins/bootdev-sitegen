from htmlnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, comp):
        if self.text == comp.text and self.text_type == comp.text_type and self.url == comp.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html_node(self):
        match self.text_type:
            case "text":
                return LeafNode(value = self.text)
            case "bold":
                return LeafNode(tag = "b", value = self.text)
            case "italics":
                return LeafNode(tag = "i", value = self.text)
            case "code":
                return LeafNode(tag = "code", value = self.text)
            case "link":
                return LeafNode(tag = "a", value = self.text, props = {"href": self.url}) 
            case "image":
                return LeafNode(tag= "img", value = "", props = {"src": self.url, "alt" : self.text}) 
            case _:
                raise Exception(f"Attempted to provide a text_node type not recognized by html conversion: {self.text_type}")
    

def main():
    pass

main()
