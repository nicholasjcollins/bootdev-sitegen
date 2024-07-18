import unittest
from textnode import TextNode
from main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a node", "normal")
        node2 = TextNode("This is a different node", "normal")
        self.assertNotEqual(node, node2)

    def test_print(self):
        node = TextNode("Test", "bold", "url")
        expected = "TextNode(Test, bold, url)"
        self.assertEqual(str(node), expected)

    def test_image_conversion(self):
        node = TextNode(text = "Alt Text", text_type = "image", url = "http://test.jpg")
        expected = "<img src=\"http://test.jpg\" alt=\"Alt Text\">"
        self.assertEqual(text_node_to_html_node(node).to_html(), expected)

    def test_link_conversion(self):
        node = TextNode(text = "Click Me", text_type = "link", url = "http://test.com")
        expected = "<a href=\"http://test.com\">Click Me</a>"
        self.assertEqual(text_node_to_html_node(node).to_html(), expected)

if __name__ == "__main__":
    unittest.main()
