from extractors import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(
  old_nodes: list[TextNode], delimiter: str | None, text_type: TextType
):
  if delimiter is None or delimiter == "":
    raise Exception(
      "Function split_nodes_delimiter must have a defined, non-empty delimiter"
    )

  if text_type not in TextType:
    raise Exception("Not a valid TextType")

  new_nodes: list[TextNode] = []

  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
    texts = node.text.split(delimiter)
    # If matching delimiter is not found, raise error
    if len(texts) % 2 == 0:
      raise Exception("Invalid Markdown syntax")
    # If matching delimiter is found, add node
    else:
      for i, text in enumerate(texts):
        # If empty text then no need to append
        if text == "":
          continue
        # For even indexes, append non-text type TextNode
        if i % 2 != 0:
          new_nodes.append(TextNode(text, text_type))
        # For odd indexes, append text type TextNode
        else:
          new_nodes.append(TextNode(text, TextType.TEXT))
  return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
  result_nodes: list[TextNode] = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      result_nodes.append(node)
      continue
    current_text = node.text
    links = extract_markdown_links(current_text)
    if len(links) == 0:
      result_nodes.append(node)
      continue
    for link in links:
      sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
      if len(sections) != 2:
        raise Exception("Invalid Markdown link: link not enclosed")
      if sections[0] != "":
        result_nodes.append(TextNode(sections[0], TextType.TEXT))
      result_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
      current_text = sections[1]
    if current_text != "":
      result_nodes.append(TextNode(current_text, TextType.TEXT))
  return result_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
  result_nodes: list[TextNode] = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      result_nodes.append(node)
      continue
    current_text = node.text
    images = extract_markdown_images(current_text)
    if len(images) == 0:
      result_nodes.append(node)
      continue
    for image in images:
      sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
      if len(sections) != 2:
        raise Exception("Invalid Markdown image: image not enclosed")
      if sections[0] != "":
        result_nodes.append(TextNode(sections[0], TextType.TEXT))
      result_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
      current_text = sections[1]
    if current_text != "":
      result_nodes.append(TextNode(current_text, TextType.TEXT))
  return result_nodes


def text_to_textnodes(text: str | None):
  if text == "" or text is None:
    raise Exception("Text cannot be empty or None")
  start_textnode = [TextNode(text, TextType.TEXT)]
  new_nodes = split_nodes_delimiter(start_textnode, "**", TextType.BOLD)
  new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
  new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
  new_nodes = split_nodes_image(new_nodes)
  new_nodes = split_nodes_link(new_nodes)
  return new_nodes
