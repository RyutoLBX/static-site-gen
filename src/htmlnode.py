class HTMLNode():
  def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None) -> None:
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def __repr__(self) -> str:
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
  
  def __eq__(self, other: object) -> bool:
    if other == None:
      return False
    if not isinstance(other, HTMLNode):
      return False
    is_equal: bool = (self.tag == other.tag) and (self.value == other.value) and (self.children == other.children) and (self.props == other.props)
    return is_equal

  def to_html(self) -> str:
    raise NotImplementedError("Method must be implemented")

  def props_to_html(self) -> str:
    if self.props == None:
      return ""
    
    props_html_text = ""
    props_count = len(self.props)

    for i, prop in enumerate(self.props):
      props_html_text += f"{prop}=\"{self.props[prop]}\""
      # If last property then no space inserted
      if i < props_count - 1:
        props_html_text += " "
    return props_html_text


class ParentNode(HTMLNode):
  def __init__(self, tag: str, children: list["HTMLNode"] | None, props: dict[str, str] | None = None) -> None:
    super().__init__(tag, None, children, props)
  
  def to_html(self) -> str:
    if self.tag == None:
      raise ValueError("All parent nodes must have a tag")
    
    if self.children == None:
      raise ValueError("All parent nodes must have children")
    
    html_text: str = ""
    for child in self.children:
      html_text += child.to_html()
    
    return f"<{self.tag}{"" if self.props == None else " "}{self.props_to_html()}>" + html_text + f"</{self.tag}>"


class LeafNode(HTMLNode):
  def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
    super().__init__(tag, value, None, props)

  def to_html(self) -> str:
    if self.value == None:
      raise ValueError("All leaf nodes must have a value")

    if self.tag == None:
      return self.value

    return f"<{self.tag}{"" if self.props == None else " "}{self.props_to_html()}>{self.value}</{self.tag}>"
