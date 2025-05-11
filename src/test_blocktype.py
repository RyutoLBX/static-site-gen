import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks

class TestBlockType(unittest.TestCase):
  def test_block_to_block_type_heading(self):
    blocks = [
      "No heading",
      "# Heading 1",
      "## Heading 2",
      "### Heading 3",
      "#### Heading 4",
      "##### Heading 5",
      "###### Heading 6",
      "####### Heading 7",
    ]
    expected_result = [
      BlockType.PARAGRAPH,
      BlockType.HEADING,
      BlockType.HEADING,
      BlockType.HEADING,
      BlockType.HEADING,
      BlockType.HEADING,
      BlockType.HEADING,
      BlockType.PARAGRAPH
    ]
    processed: list[BlockType] = []
    for block in blocks:
      processed.append(block_to_block_type(block))
    
    self.assertListEqual(processed, expected_result)

  def test_block_to_block_type_code(self):
    blocks = [
      "No code\nAt all",
      "``\nincorrect format\n``",
      "```\ncorrectly\n formatted block\n```",
      "```\nincorrectly formatted\nmultiline block\n``",
      "```\ncorrectly formatted\nmultiline block\n```",
    ]
    expected_result = [
      BlockType.PARAGRAPH,
      BlockType.PARAGRAPH,
      BlockType.CODE,
      BlockType.PARAGRAPH,
      BlockType.CODE
    ]
    processed: list[BlockType] = []
    for block in blocks:
      processed.append(block_to_block_type(block))
    
    self.assertListEqual(processed, expected_result)

  def test_block_to_block_type_quote(self):
    blocks = [
      "No quote",
      "> Single line quote",
      "> Multi\n> Line\n> Quote",
      "> Oh I forgot\nTo put a quote marker here"
    ]
    expected_result = [
      BlockType.PARAGRAPH,
      BlockType.QUOTE,
      BlockType.QUOTE,
      BlockType.PARAGRAPH,
    ]
    processed: list[BlockType] = []
    for block in blocks:
      processed.append(block_to_block_type(block))
    
    self.assertListEqual(processed, expected_result)

  def test_block_to_block_type_ulist(self):
    blocks = [
      "- This is an unordered list item entry",
      "No list",
      "- \n- ",
      "- This is a list\nThis is the second item"
    ]
    expected_result = [
      BlockType.ULIST,
      BlockType.PARAGRAPH,
      BlockType.ULIST,
      BlockType.PARAGRAPH
    ]
    processed: list[BlockType] = []
    for block in blocks:
      processed.append(block_to_block_type(block))
    
    self.assertListEqual(processed, expected_result)


  def test_block_to_block_type_olist(self):
    blocks = [
      "A. This is a list\nB. This is the second item",
      "1. This is a list\n2. This is the second item",
      "1. This is a list\n2. This is the second item\n3. This is the third item\n4. This is the fourth item\n5. This is the fifth item",
      "1. This is a list\n1. This is the second item",
      "1. This is a list\n999. This is the second item"
    ]
    expected_result = [
      BlockType.PARAGRAPH,
      BlockType.OLIST,
      BlockType.OLIST,
      BlockType.PARAGRAPH,
      BlockType.PARAGRAPH
    ]
    processed: list[BlockType] = []
    for block in blocks:
      processed.append(block_to_block_type(block))

    self.assertListEqual(processed, expected_result)

  # TEST FOR SPLITTING BLOCKS
  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
      ],
    )

  def test_markdown_to_blocks_empty_blocks(self):
    md = """
# Heading Text

This is a **bolded** paragraph



This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
This is still within the same block.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "# Heading Text",
        "This is a **bolded** paragraph",
        "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\nThis is still within the same block.",
        "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
      ],
    )

  def test_markdown_to_blocks_so_many_whitespaces(self):
    md = """
# Heading Text








                      This is a **bolded** paragraph        



               This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
This is still within the same block.                         


This is a different block! It even has some code in it: `print("hello world")`



          - This is the first list item in a list block
- This is a list item
- This is another list item            
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "# Heading Text",
        "This is a **bolded** paragraph",
        "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\nThis is still within the same block.",
        "This is a different block! It even has some code in it: `print(\"hello world\")`",
        "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
      ],
    )
