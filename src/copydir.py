import os
import shutil


def copy_recursive(source: str, dest: str):
  if dest == "./docs":
    shutil.rmtree("./docs")
  if not os.path.exists("./docs"):
    os.mkdir("./docs")

  filenames = os.listdir(source)

  for item in filenames:
    current_source = f"{source}/{item}"
    if os.path.isfile(current_source):
      shutil.copy(current_source, dest)
    else:
      os.mkdir(f"{dest}/{item}")
      copy_recursive(current_source, f"{dest}/{item}")
