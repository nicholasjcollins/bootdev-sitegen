import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={"href":"http://test.com","target":"_blank"})
        expected = " href=\"http://test.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected)
    
    def test_empty_props(self):
        node = HTMLNode()
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_print(self):
        node = HTMLNode("tag", "value")
        expected = "HTMLNode(tag, value, None, None)"
        self.assertEqual(str(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_node(self):
        node = LeafNode(tag = "a", value = "Click Here!", props={"href":"http://test.test"})
        expected = "<a href=\"http://test.test\">Click Here!</a>"
        self.assertEqual(node.to_html(), expected)

    def test_value_only(self):
        node = LeafNode(value = "This is some plain stuff")
        expected = "This is some plain stuff"
        self.assertEqual(node.to_html(), expected)

class TestParentNode(unittest.TestCase):
    def test_basic_node(self):
        child_node = LeafNode(value = "This is just a sentence.")
        parent_node = ParentNode(tag = "p", children=[child_node])
        expected = "<p>This is just a sentence.</p>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_recursive_node(self):
        child_node = LeafNode(tag = "a", value = "Link", props={"href":"http://test.test"})
        child_node2 = LeafNode(value = "Just a sentence")
        sub_parent_node = ParentNode(tag = "i", children = [child_node, child_node2])
        child_node3 = LeafNode(value = "Another Sentence")
        parent_node = ParentNode(tag = "p", children = [sub_parent_node, child_node3], props={"test":"prop-test"})
        expected = "<p test=\"prop-test\"><i><a href=\"http://test.test\">Link</a>Just a sentence</i>Another Sentence</p>"
        self.assertEqual(parent_node.to_html(), expected)
                        
if __name__ == "__main__":
    unittest.main()
