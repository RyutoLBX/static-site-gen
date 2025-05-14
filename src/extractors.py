import re

def extract_markdown_images(markdown: str):
  match_text = r"!\[(.+?)\]\((.+?)\)"
  matches = re.findall(match_text, markdown)
  return matches

def extract_markdown_links(markdown: str):
  match_text = r"(?<!\!)\[(.+?)\]\((.+?)\)"
  matches = re.findall(match_text, markdown)
  return matches

def extract_markdown_title(markdown: str):
  lines = markdown.split("\n")
  for line in lines:
    if line.startswith("# "):
      return line[1:].strip()
  raise Exception("No title was found")