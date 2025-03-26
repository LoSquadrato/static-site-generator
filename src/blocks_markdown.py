from enum import Enum

from inline_markdown import *
from htmlnode import ParentNode
from textnode import TextNode, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "text"
    HEADING = "#"
    CODE = "`"
    QUOTE = ">"
    UNORDERED_LIST = "-"
    ORDERED_LIST = "1."


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH           


def markdown_to_blocks(markdown):
    result = []
    md_blocks = markdown.split("\n\n") 
    for block in md_blocks:
        strip_block = block.strip("\n ")
        if strip_block == "":
            continue
        if "\n" in strip_block:
            nline_block = strip_block.split("\n")
            stripped_line = list(map(lambda x: x.strip(), nline_block))
            joined_line = "\n".join(stripped_line)
            result.append(joined_line)    
        if "\n" not in strip_block:
            result.append(strip_block)       
    return result

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    html_list = [] 
    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(paragraph_to_html(block))
            h_node = ParentNode("p", children)
            html_list.append(h_node)
            continue
        if block_type == BlockType.HEADING:
            h_tag = f"h{block.count("#",0 ,6)}"
            children = text_to_children(heading_to_html(block))
            h_node = ParentNode(h_tag, children)
            html_list.append(h_node)
            continue
        if block_type == BlockType.QUOTE:
            children = text_to_children(quote_to_html(block))
            h_node = ParentNode("blockquote", children)
            html_list.append(h_node)
            continue
        if block_type == BlockType.CODE:
            code_node = text_node_to_html_node(TextNode(code_to_html(block), TextType.CODE))
            h_node = ParentNode("pre", [code_node])
            html_list.append(h_node)
            continue
        if block_type == BlockType.UNORDERED_LIST:
            children = unordered_list_to_html_node(block)
            h_node = ParentNode("ul", children)
            html_list.append(h_node)
            continue
        if block_type == BlockType.ORDERED_LIST:
            children = ordered_list_to_html_node(block)
            h_node = ParentNode("ol", children)
            html_list.append(h_node)
            continue
    return ParentNode("div", html_list)
        
def unordered_list_to_html_node(text):
    lines = text.split("\n")
    line_nodes = []
    for line in lines:
        strip_line = line.replace("- ", "", 1)
        children = text_to_children(strip_line)
        line_node = ParentNode("li", children)
        line_nodes.append(line_node)  
    return line_nodes


def ordered_list_to_html_node(text):
    lines = text.split("\n")
    line_nodes = []
    i = 0
    for line in lines:
        i += 1
        strip_line = line.lstrip(f"{i}. ")
        children = text_to_children(strip_line)
        line_node = ParentNode("li", children)
        line_nodes.append(line_node)  
    return line_nodes

def paragraph_to_html(text):
    strip_txt = text.replace("\n", " ")
    return strip_txt

def heading_to_html(text):
    strip_txt = text.lstrip("# ")
    return strip_txt

def code_to_html(text):
    lines = text.split("\n")
    strip_txt = []
    for line in lines:
        if "```" in line:
            continue
        strip_txt.append(line)
    code_txt = "\n".join(strip_txt)
    return code_txt

def quote_to_html(text):
    strip_txt = text.lstrip("> ")
    return strip_txt

def text_to_children(text):
    nodes = text_to_textnodes(text)
    children_node = []
    for node in nodes:
        result = text_node_to_html_node(node)
        children_node.append(result)
    return children_node

