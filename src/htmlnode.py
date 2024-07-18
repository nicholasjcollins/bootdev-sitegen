class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        str = ""
        if self.props == None: return str
        for key in self.props:
            str += f" {key}=\"{self.props[key]}\""
        return str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        if value == None:
            raise ValueError("LeafNode requires a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag == None:
            return self.value
        closing_tag = ""
        if self.tag != "img": closing_tag = f"</{self.tag}>"
        return f"<{self.tag + self.props_to_html()}>{self.value}" + closing_tag


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode requires a tag")
        if self.children== None:
            raise ValueError("ParentNode requires children")
        str = f"<{self.tag + self.props_to_html()}>"
        for child in self.children:
            str += f"{child.to_html()}"
        str += f"</{self.tag}>"
        return str
