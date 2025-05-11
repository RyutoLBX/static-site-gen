import os, shutil
from generatepage import generate_pages_recursive

def copy_static_to_public(source: str = "./static", dest: str = "./public"):
  if dest == "./public":
    shutil.rmtree(dest)
  if not os.path.exists("./public"):
    os.mkdir("./public")
  filenames = os.listdir(source)
  
  for item in filenames:
    current_source = f"{source}/{item}"
    if os.path.isfile(current_source):
      shutil.copy(current_source, dest)
    else:
      os.mkdir(f"{dest}/{item}")
      copy_static_to_public(current_source, f"{dest}/{item}")
  return

def main():
  copy_static_to_public("./static", "./public")
  generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
  main()
