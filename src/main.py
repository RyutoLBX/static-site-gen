import sys
from copydir import copy_recursive
from generatepage import generate_pages_recursive

def main():
  base_path = "/"
  if len(sys.argv) > 1:
    base_path = sys.argv[1]

  copy_recursive("./static", "./docs")
  generate_pages_recursive("./content", "./template.html", "./docs", base_path)

if __name__ == "__main__":
  main()
