import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestTextNode(unittest.TestCase):
  # HTML NODE TESTS
  def test_eq(self):
    node1 = HTMLNode(None, "This is a HTML node", None, None)
    node2 = HTMLNode(None, "This is a HTML node", None, None)
    self.assertEqual(node1, node2)

  def test_not_eq_tag(self):
    node1 = HTMLNode("h1", "Link to Google", None, None)
    node2 = HTMLNode("h2", "Link to Google", None, None)
    self.assertNotEqual(node1, node2)

  def test_not_eq_val(self):
    node1 = HTMLNode(None, "This is content A", None, None)
    node2 = HTMLNode(None, "This is content B", None, None)
    self.assertNotEqual(node1, node2)

  def test_eq_with_child(self):
    child1 = HTMLNode("h2", "Content Header", None, None)
    child2 = HTMLNode("h2", "Content Header", None, None)
    node1 = HTMLNode("h1", "Title", child1, None)
    node2 = HTMLNode("h1", "Title", child2, None)
    self.assertEqual(node1, node2)

  def test_not_eq_child(self):
    child1 = HTMLNode("h2", "Content Header", None, None)
    node1 = HTMLNode("h1", "Title", child1, None)
    node2 = HTMLNode("h1", "Title", None, None)
    self.assertNotEqual(node1, node2)

  def test_eq_props(self):
    props1 = {"href": "https://www.google.com", "target": "_blank"}
    props2 = {"href": "https://www.google.com", "target": "_blank"}
    node1 = HTMLNode("a", "Link to Google", None, props1)
    node2 = HTMLNode("a", "Link to Google", None, props2)
    self.assertEqual(node1, node2)

  def test_not_eq_props(self):
    props1 = {"href": "https://www.google.com", "target": "_blank"}
    props2 = {"href": "https://www.yahoo.com", "target": "_blank"}
    node1 = HTMLNode("a", "Link here", None, props1)
    node2 = HTMLNode("a", "Link here", None, props2)
    self.assertNotEqual(node1, node2)

  # LEAF NODE TESTS
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_h1(self):
    node = LeafNode("h1", "Hello, world!")
    self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

  def test_leaf_to_html_props(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

  # PARENT NODE TESTS
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span><b>grandchild</b></span></div>",
    )
    
  def test_to_html_with_great_grandchildren(self):
    great_grandchild_node = LeafNode("b", "great grandchild")
    grandchild_node = ParentNode("i", [great_grandchild_node])
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span><i><b>great grandchild</b></i></span></div>",
    )

  def test_to_html_with_children_and_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    child_node2 = LeafNode("a", "Click here!", {"href": "https://google.com"})
    parent_node = ParentNode("div", [child_node, child_node2])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span><b>grandchild</b></span><a href=\"https://google.com\">Click here!</a></div>",
    )
  
if __name__ == "__main__":
  unittest.main()