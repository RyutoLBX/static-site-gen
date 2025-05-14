from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks
from splitnodes import text_to_textnodes
from htmlnode import ParentNode, LeafNode, HTMLNode
from texttohtmlnode import text_node_to_html_node

def markdown_to_html_node(markdown: str):
  blocks = markdown_to_blocks(markdown)

  html_nodes: list[HTMLNode] = []
  node: HTMLNode
  for block in blocks:
    block_type = block_to_block_type(block)
    match block_type:
      # Paragraph block:
      # This is a paragraph with **bold** text and _italic_ text
      case BlockType.PARAGRAPH:
        inline_nodes: list[HTMLNode] = []
        lines = block.split("\n")
        for i, line in enumerate(lines):
          if i != len(lines) - 1:
            line += " "
          text_nodes = text_to_textnodes(line)
          for text_node in text_nodes:
            inline_nodes.append(text_node_to_html_node(text_node))
        node = ParentNode("p", inline_nodes)

      # Heading block (CAN HAVE INLINES):
      # <h1>This is a heading</h1>
      case BlockType.HEADING:
        sections = block.split(" ", 1)
        heading_no = sections[0].count("#")

        inline_nodes: list[HTMLNode] = []
        text_nodes = text_to_textnodes(sections[1])
        for text_node in text_nodes:
          inline_nodes.append(text_node_to_html_node(text_node))
        node = ParentNode(f"h{heading_no}", inline_nodes)

      # Code block:
      # ```
      # This is a code block
      # ```
      case BlockType.CODE:
        sections = block.split("```", 2)
        node = ParentNode("pre", [LeafNode("code", sections[1].strip())])

      # Quote block:
      # > This is a quote block
      # > This is the same quote block
      case BlockType.QUOTE:
        lines = block.split("\n")
        processed_text = ""
        for i, line in enumerate(lines):
          line = line.replace(">", "").strip()
          if i >= 1:
            processed_text += " "
          processed_text += line
        node = LeafNode("blockquote", processed_text)

      # Unordered list block:
      # - This is an item
      # - This is another item
      case BlockType.ULIST:
        list_nodes: list[HTMLNode] = []
        lines = block.split("\n")
        for line in lines:
          sections = line.split("- ", 1)
          if len(sections) != 2:
            raise Exception("Malformed list")
          text_nodes = text_to_textnodes(sections[1])
          inline_nodes: list[HTMLNode] = []
          for text_node in text_nodes:
            inline_nodes.append(text_node_to_html_node(text_node))
          list_nodes.append(ParentNode("li", inline_nodes))
        node = ParentNode("ul", list_nodes)

      # Ordered list block:
      # 1. This is an item
      # 2. This is another item
      case BlockType.OLIST:
        list_nodes: list[HTMLNode] = []
        lines = block.split("\n")
        for line in lines:
          sections = line.split(". ", 1)
          if len(sections) != 2:
            raise Exception("Malformed list")
          text_nodes = text_to_textnodes(sections[1])
          inline_nodes: list[HTMLNode] = []
          for text_node in text_nodes:
            inline_nodes.append(text_node_to_html_node(text_node))
          list_nodes.append(ParentNode("li", inline_nodes))
        node = ParentNode("ol", list_nodes)
    html_nodes.append(node)
  
  parent_node = ParentNode("div", html_nodes)
  return parent_node
