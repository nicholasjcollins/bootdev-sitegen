import unittest
from textnode import TextNode
from markdown_parser import *

class TestMarkdownParser(unittest.TestCase):

    def test_bold_parse(self):
        test_string = "This is a string with **bold text**, *italics text*, and a `code block`"
        test_node = TextNode(text = test_string, text_type = "text")
        parsed_text = split_nodes_delimiter([test_node], "**")
        expected_case_1 = "This is a string with "
        expected_case_2 = "bold text"
        expected_case_3 = "bold"
        self.assertEqual(parsed_text[0].text, expected_case_1)
        self.assertEqual(parsed_text[1].text, expected_case_2)
        self.assertEqual(parsed_text[1].text_type, expected_case_3)

    def test_italics_parse(self):
        test_string = "*This is an entire italics block.*"
        test_node = TextNode(text = test_string, text_type = "text")
        parsed_text = split_nodes_delimiter([test_node], "*")
        expected_length = 1
        expected_string = "This is an entire italics block."

        print(parsed_text)
        self.assertEqual(len(parsed_text), expected_length)
        self.assertEqual(parsed_text[0].text, expected_string)

    def text_image_extract(self):
        test_string = "This is a string with an ![Alt Text](http://image.jpg)"
        return_list = extract_markdown_images(test_string)
        self.assertEqual(return_list[0][0], "Alt Text")
        self.assertEqual(return_list[0][1], "http://image.jpg")


    def text_link_extract(self):
        test_string = "This is a string with a [Hyperlink](http://link.com)"
        return_list = extract_markdown_links(test_string)
        self.assertEqual(return_list[0][0], "Hyperlink")
        self.assertEqual(return_list[0][1], "http://link.com")

    def test_image_split(self):
        test_list = [
            TextNode(text = "This node has an image here: ![With Alt Text](http://url.url) and here: ![More Alt Text](http://test.jpg) and some more stuff after", text_type = "text"),
            TextNode(text = "![Alt Test](http://test.jpg) This starts with an image", text_type = "text"),
            TextNode(text = "This ends with an image ![Something](http://something.png)", text_type = "text")
        ]
        output = split_nodes_links_images(test_list, True)
        self.assertEqual(output[1].url, "http://url.url")
        self.assertEqual(output[4].text, " and some more stuff after")

    def test_link_split(self):
        test_list = [TextNode(text = "This node has a link [Click Me](to.go.here)", text_type = "text")]
        output = split_nodes_links_images(test_list, False)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[1].url, "to.go.here")

    def test_text_parse(self):
        str = "This is some test markdown with **bold** and *italics* text. It also has a `code block here` and one image: ![With This Alt Text](http://at.this.loc) and a link: [Right Here](that.goes.here)"
        output = text_to_text_nodes(str)
        self.assertEqual(len(output), 10)
        self.assertEqual(output[9].url, "that.goes.here")
        self.assertEqual(output[1].text_type, "bold")


    str = """
# Header


## Another Header with too many blank lines

This is just a simple section of text.

Here's a section of text with another line on it.
This should be a part of the above.

* List Item 1
* List Item 2
* List Item 3

     No Leading or Trailing Whitespace     

1. Ordered List 1
2. Ordered List 2
3. Ordered List 3

```
this is some code I think
maybe an extra line of code
```
"""

    test_blocks = markdown_to_blocks(str)

    def test_block_count(self):
        self.assertEqual(len(self.test_blocks),8)

    def test_bad_lines(self):
        expected_index_0 = "# Header"
        expected_index_1 = "## Another Header with too many blank lines"
        self.assertEqual(self.test_blocks[0], expected_index_0)
        self.assertEqual(self.test_blocks[1], expected_index_1)

    def test_markdown_block_list(self):
        expected_list="* List Item 1\n* List Item 2\n* List Item 3"
        self.assertEqual(self.test_blocks[4], expected_list)

    def test_md_unordered_list_id(self):
        self.assertEqual(block_to_block_type(self.test_blocks[4]), "unordered_list")

    def test_md_ordered_list_id(self):
        self.assertEqual(block_to_block_type(self.test_blocks[6]), "ordered_list")

    def test_md_code_block_id(self):
        self.assertEqual(block_to_block_type(self.test_blocks[7]), "code")

    def test_md_paragraph_id(self):
        self.assertEqual(block_to_block_type(self.test_blocks[2]), "paragraph")  
        self.assertEqual(block_to_block_type(self.test_blocks[3]), "paragraph")
        self.assertEqual(block_to_block_type(self.test_blocks[5]), "paragraph")

    def test_md_header_id(self):
        self.assertEqual(block_to_block_type(self.test_blocks[0]), "heading")
        self.assertEqual(block_to_block_type(self.test_blocks[1]), "heading")

    def test_md_header_block_to_html(self):
        "# This is a header block"

    test_data_3 = """
# Title

## Subheading

>Block Quote With **bold emphasis**
>on one of the lines.

```
def maybe(some_code):
that_looks = like_this
```

## Another Subheading

With just another paragraph of stuff beneath it. That's not so bad.

### An H3 block

- With a list
- Of Items
- Like this

### Another H3 Block

1. This time
2. With an ordered
3. List
"""
    html_nodes = convert_markdown(test_data_3)

    def test_html_node_parent_wrapper(self):
        self.assertEqual(self.html_nodes.tag, "div")

    def test_child_node_1(self):
        self.assertEqual(self.html_nodes.children[0].tag, "h1")
        self.assertEqual(self.html_nodes.children[0].children[0].value, "Title")

    def test_inline_within_block(self):
        self.assertEqual(self.html_nodes.children[2].children[1].tag, "b")

    def test_extract_title(self):
        self.assertEqual(extract_title(self.test_data_3), "Title")



