import unittest

from textnode import TextNode, TextType
from texttohtmlnode import text_node_to_html_node
from splitnodes import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
  def test_bold_inline(self):
    old_nodes = [TextNode("This is a passage with **bold** text", TextType.TEXT)]
    new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    self.assertEqual(new_nodes[0], TextNode("This is a passage with ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
    self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

  def test_bold_inline_edge(self):
    old_nodes = [TextNode("**Wow!** So many **bold texts!**", TextType.TEXT)]
    new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    self.assertEqual(new_nodes[0], TextNode("Wow!", TextType.BOLD))
    self.assertEqual(new_nodes[1], TextNode(" So many ", TextType.TEXT))
    self.assertEqual(new_nodes[2], TextNode("bold texts!", TextType.BOLD))

  def test_italic_inline(self):
    old_nodes = [TextNode("This is a passage with _italic_ text", TextType.TEXT)]
    new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
    self.assertEqual(new_nodes[0], TextNode("This is a passage with ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
    self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

  def test_code_inline(self):
    old_nodes = [TextNode("This is a passage with `code` text", TextType.TEXT)]
    new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
    self.assertEqual(new_nodes[0], TextNode("This is a passage with ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
    self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

  def test_no_nodes(self):
    old_nodes: list[TextNode] = []
    new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    self.assertEqual(new_nodes, [])

  def test_none_delimiter(self):
    old_nodes = [TextNode("Test passage with **bold** word", TextType.TEXT)]
    self.assertRaises(Exception, split_nodes_delimiter, (old_nodes, None, TextType.BOLD))

  def test_empty_delimiter(self):
    old_nodes = [TextNode("Test passage with **bold** word", TextType.TEXT)]
    self.assertRaises(Exception, split_nodes_delimiter, (old_nodes, "", TextType.BOLD))

  def test_invalid_type(self):
    old_nodes = [TextNode("Test passage with **bold** word", TextType.TEXT)]
    self.assertRaises(Exception, split_nodes_delimiter, (old_nodes, "", None))

  def test_multiple_nodes(self):
    old_nodes = [
      TextNode("This is a passage with **bold** text!", TextType.TEXT),
      TextNode("This is a passage with no bold text!", TextType.TEXT),
      TextNode("This is a passage with **bold** text again!", TextType.TEXT),
      TextNode("This is another passage with zero bold text!", TextType.TEXT)
    ]
    new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    self.assertEqual(new_nodes[0], TextNode("This is a passage with ", TextType.TEXT))
    self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
    self.assertEqual(new_nodes[2], TextNode(" text!", TextType.TEXT))
    self.assertEqual(new_nodes[3], TextNode("This is a passage with no bold text!", TextType.TEXT))
    self.assertEqual(new_nodes[4], TextNode("This is a passage with ", TextType.TEXT))
    self.assertEqual(new_nodes[5], TextNode("bold", TextType.BOLD))
    self.assertEqual(new_nodes[6], TextNode(" text again!", TextType.TEXT))
    self.assertEqual(new_nodes[7], TextNode("This is another passage with zero bold text!", TextType.TEXT))

  # TESTS FOR SPLITTING IMAGES AND LINKS
  def test_split_images(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
      ],
      new_nodes,
    )

  def test_split_links(self):
    node = TextNode(
      "This is text with a [link](https://yahoo.com) and another [second link](https://google.com)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://yahoo.com"),
        TextNode(" and another ", TextType.TEXT),
        TextNode("second link", TextType.LINK, "https://google.com"),
      ],
      new_nodes,
    )

  def test_split_links_but_actually_image(self):
    node = TextNode(
      "This is text with no links but ![two](https://i.imgur.com/zjjcJKZ.png) ![images](https://i.imgur.com/zjjcJKZ.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with no links but ![two](https://i.imgur.com/zjjcJKZ.png) ![images](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_split_image_but_actually_link(self):
    node = TextNode(
      "This is text with no images but [two](https://yahoo.com) [links](https://google.com)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with no images but [two](https://yahoo.com) [links](https://google.com)", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_split_image_has_both_link_and_image(self):
    node = TextNode(
      "This is text with one ![image](https://i.imgur.com/zjjcJKZ.png) and one [link](https://google.com)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with one ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and one [link](https://google.com)", TextType.TEXT)
      ],
      new_nodes,
    )

  def test_split_link_has_both_link_and_image(self):
    node = TextNode(
      "This is text with one ![image](https://i.imgur.com/zjjcJKZ.png) and one [link](https://google.com) but there's more text after",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with one ![image](https://i.imgur.com/zjjcJKZ.png) and one ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://google.com"),
        TextNode(" but there's more text after", TextType.TEXT)
      ],
      new_nodes,
    )

    # TESTS FOR ALL NODE SPLITTING
  def test_split_all(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [boot dev link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    self.assertListEqual(
      [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("boot dev link", TextType.LINK, "https://boot.dev")
      ],
      new_nodes,
    )

  # TEXT NODE TO HTML NODE TESTS
  def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_bold(self):
    node = TextNode("This is a bold text node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is a bold text node")

  def test_italic(self):
    node = TextNode("This is an italic text node", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is an italic text node")

  def test_code(self):
    node = TextNode("# This is a code text node", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "# This is a code text node")

  def test_link(self):
    node = TextNode("This is a link text node", TextType.LINK, "https://google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is a link text node")
    self.assertEqual(html_node.props, {"href": "https://google.com"})

  def test_image(self):
    node = TextNode("This is an alt text for an image", TextType.IMAGE, "url/to/image")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.props, {"src": "url/to/image", "alt": "This is an alt text for an image"})

if __name__ == "__main__":
    unittest.main()
