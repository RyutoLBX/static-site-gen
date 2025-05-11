from enum import Enum

class TextType(Enum):
  TEXT = "text"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"

class TextNode():
  def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, other: object) -> bool:
    if other == None:
      return False
    if not isinstance(other, TextNode):
      return False
    is_equal: bool = (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)
    return is_equal
  
  def __repr__(self) -> str:
    return f"TextNode(\"{self.text}\", {self.text_type}, {self.url})"
