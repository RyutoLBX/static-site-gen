from textnode import TextNode, TextType

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
