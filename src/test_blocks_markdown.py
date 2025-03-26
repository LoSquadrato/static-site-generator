import unittest
from blocks_markdown import *

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_with_headingandlist(self):
        md = """
    # This is a heading

    This is a paragraph of text. It has some **bold** 
    and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold**\nand _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_with_orderlistandcode(self):
        md = """
    1. Item 1
    2. Item 2
    3. Item 3

    ```
    This is code
    ```

    > This is a quote.

    
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "1. Item 1\n2. Item 2\n3. Item 3",
                "```\nThis is code\n```",
                "> This is a quote.",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text _in_ a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text <i>in</i> a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_unordered_list(self):
        md = """
    - _Item 1 in italic_
    - **Item 2 in bold**
    - `Item 3 in code`

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><i>Item 1 in italic</i></li><li><b>Item 2 in bold</b></li><li><code>Item 3 in code</code></li></ul></div>",
        )

    def test_code_list(self):
        md = """
    ```
    This is code
    ```

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is code</code></pre></div>",
        )


    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )


    def test_heading_list(self):
        md = """
    # Heading 1

    ## Heading 2

    ### Heading 3

    #### Heading 4

    ##### Heading 5

    ###### Heading 6    

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )


    def test_quote(self):
        md = """
    > This is **quote**    

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>quote</b></blockquote></div>",
        )

    def test_ordered_list(self):
        md = """
    1. Item 1
    2. Item 2
    3. Item 3

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
