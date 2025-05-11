import os
from markdowntohtml import markdown_to_html_node
from extractors import extract_markdown_title

def generate_page(from_path: str, template_path: str, dest_path: str):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  with open(from_path) as source_file:
    source_markdown: str = source_file.read()
  with open(template_path) as template_file:
    template_html: str = template_file.read()
  
  content = markdown_to_html_node(source_markdown)
  content = content.to_html()
  title = extract_markdown_title(source_markdown)
  full_html = template_html.replace("{{ Title }}", title)
  full_html = full_html.replace("{{ Content }}", content)

  destination_file = open(dest_path, 'w')
  destination_file.write(full_html)
  return

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
  filenames = os.listdir(dir_path_content)
  for item in filenames:
    current_source = f"{dir_path_content}/{item}"
    if os.path.isfile(current_source): # if it's an md file in ./content
      generate_page(current_source, template_path, f"{dest_dir_path}/{item[:-2]}html")
    else: # if it's a directory in ./content
      if not os.path.isdir(f"{dest_dir_path}/{item}"):
        os.mkdir(f"{dest_dir_path}/{item}")
      generate_pages_recursive(current_source, template_path, f"{dest_dir_path}/{item}")
