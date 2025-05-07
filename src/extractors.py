import re

def extract_markdown_images(text):
  match_text = r"!\[(.*?)\]\((.*?)\)"
  matches = re.findall(match_text, text)
  return matches

def extract_markdown_links(text):
  match_text = r"(?<!!)\[(.*?)\]\((.*?)\)"
  matches = re.findall(match_text, text)
  return matches