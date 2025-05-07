import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNode(unittest.TestCase):
    def test_bold(self):
      old_nodes = [TextNode("This is a passage with **bold** text", TextType.TEXT)]
      new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
      self.assertEqual(new_nodes[0], TextNode("This is a passage with ", TextType.TEXT))
      self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
      self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_bold_edge(self):
      old_nodes = [TextNode("**Wow!** So many **bold texts!**", TextType.TEXT)]
      new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
      self.assertEqual(new_nodes[0], TextNode("Wow!", TextType.BOLD))
      self.assertEqual(new_nodes[1], TextNode(" So many ", TextType.TEXT))
      self.assertEqual(new_nodes[2], TextNode("bold texts!", TextType.BOLD))

    def test_italic(self):
      old_nodes = [TextNode("This is a passage with _italic_ text", TextType.TEXT)]
      new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
      self.assertEqual(new_nodes[0], TextNode("This is a passage with ", TextType.TEXT))
      self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
      self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_code(self):
      old_nodes = [TextNode("This is a passage with `code` text", TextType.TEXT)]
      new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
      self.assertEqual(new_nodes[0], TextNode("This is a passage with ", TextType.TEXT))
      self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
      self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_no_nodes(self):
       old_nodes = []
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

if __name__ == "__main__":
    unittest.main()