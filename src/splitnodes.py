from textnode import TextNode, TextType
from extractors import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  if delimiter == None or delimiter == "":
    raise Exception("Function split_nodes_delimiter must have a defined, non-empty delimiter")

  if text_type not in TextType:
    raise Exception("Not a valid TextType")
  
  new_nodes = []

  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
    else:
      texts = node.text.split(delimiter)
      # If matching delimiter is not found, raise error
      if len(texts) % 2 == 0:
        raise Exception("Invalid Markdown syntax")
      # If matching delimiter is not found, raise error
      else:
        for i, text in enumerate(texts):
          # If empty text then no need to append
          if text == "":
            continue
          # For even indexes, append non-text type node
          if i % 2 != 0:
            new_nodes.append(TextNode(text, text_type))
          # For odd indexes, append non-text type node
          else:
            new_nodes.append(TextNode(text, TextType.TEXT))

  return new_nodes


def split_nodes_link(old_nodes):
  match_strings = ["[", "](", ")"]
  new_nodes = []
  texts = []

  for node in old_nodes:
    text = node.text
    links = extract_markdown_links(text)
    if len(links) == 0:
      return old_nodes
    for i in range(len(links)):
      texts.append(text.split(match_strings[0], 1)[0])
      text = text[len(texts[0 + 3 * i]) + len(match_strings[0]):]
      texts.append(text.split(match_strings[1], 1)[0])
      text = text[len(texts[1 + 3 * i]) + len(match_strings[1]):]
      texts.append(text.split(match_strings[2], 1)[0])
      text = text[len(texts[2 + 3 * i]) + len(match_strings[2]):]

  i = 0
  while i in range(len(texts)):
    # If empty text then do not append
    if texts[i] == "":
      continue
    text_type = TextType.TEXT if i % 3 == 0 else TextType.LINK
    if text_type == TextType.TEXT:
      new_nodes.append(TextNode(texts[i], text_type))
      i += 1
    else:
      new_nodes.append(TextNode(texts[i], text_type, texts[i+1]))
      i += 2
  return new_nodes


def split_nodes_image(old_nodes):
  match_strings = ["![", "](", ")"]
  new_nodes = []
  texts = []

  for node in old_nodes:
    text = node.text
    images = extract_markdown_images(text)
    if len(images) == 0:
      return old_nodes
    for i in range(len(images)):
      texts.append(text.split(match_strings[0], 1)[0])
      text = text[len(texts[0 + 3 * i]) + len(match_strings[0]):]
      texts.append(text.split(match_strings[1], 1)[0])
      text = text[len(texts[1 + 3 * i]) + len(match_strings[1]):]
      texts.append(text.split(match_strings[2], 1)[0])
      text = text[len(texts[2 + 3 * i]) + len(match_strings[2]):]

  i = 0
  while i in range(len(texts)):
    # If empty text then do not append
    if texts[i] == "":
      continue
    text_type = TextType.TEXT if i % 3 == 0 else TextType.IMAGE
    if text_type == TextType.TEXT:
      new_nodes.append(TextNode(texts[i], text_type))
      i += 1
    else:
      new_nodes.append(TextNode(texts[i], text_type, texts[i+1]))
      i += 2

  return new_nodes
