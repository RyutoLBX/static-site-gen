import unittest

from markdowntohtml import markdown_to_html_node

class TestExtractors(unittest.TestCase):
  def test_paragraphs(self):
    md = """
Example **bolded** paragraph
text

Second paragraph, _italic_ and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>Example <b>bolded</b> paragraph text</p><p>Second paragraph, <i>italic</i> and <code>code</code> here</p></div>",
    )

  def test_codeblock(self):
    md = """
```
This text _should_ stay
the **same**
```

```
code block
code block 2 electric boogaloo
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><pre><code>This text _should_ stay\nthe **same**</code></pre><pre><code>code block\ncode block 2 electric boogaloo</code></pre></div>",
    )

  def test_heading(self):
    md = """# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
    )

  def test_image_and_link(self):
    md = "Oh no this text has an ![image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://example.com)!"

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>Oh no this text has an <img src=\"https://i.imgur.com/fJRm4Vk.jpeg\" alt=\"image\"></img> and a <a href=\"https://example.com\">link</a>!</p></div>",
    )

  def test_all_inline(self):
    md = "Full test of all inline functions: **bold**, _italic_, `code`, and also an image ![image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://example.com)!"

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>Full test of all inline functions: <b>bold</b>, <i>italic</i>, <code>code</code>, and also an image <img src=\"https://i.imgur.com/fJRm4Vk.jpeg\" alt=\"image\"></img> and a <a href=\"https://example.com\">link</a>!</p></div>",
    )

  def test_unordered_list(self):
    md = """Let's make an unordered list!!!

- this is an item
- this is an item
- this is an item"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>Let's make an unordered list!!!</p><ul><li>this is an item</li><li>this is an item</li><li>this is an item</li></ul></div>",
    )

  def test_ordered_list(self):
    md = """Ordered lists are actually better!

1. ordered item
2. ordered item
3. ordered item"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>Ordered lists are actually better!</p><ol><li>ordered item</li><li>ordered item</li><li>ordered item</li></ol></div>",
    )

  def test_inline_markdown_in_headings(self):
    md = """# This is **Important**, You Know..."""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h1>This is <b>Important</b>, You Know...</h1></div>",
    )

if __name__ == "__main__":
    unittest.main()