from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
  if text_node.text_type not in TextType:
    raise Exception("Unexpected text type")
  match text_node.text_type:
    case TextType.TEXT:
      return LeafNode(None, text_node.text, None)
    case TextType.BOLD:
      return LeafNode("b", text_node.text, None)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text, None)
    case TextType.CODE:
      return LeafNode("code", text_node.text, None)
    case TextType.LINK:
      return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
    case TextType.IMAGE:
      return LeafNode(
        "img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"}
      )
