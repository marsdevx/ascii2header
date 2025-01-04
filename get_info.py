import os
import subprocess
from datetime import datetime

def get_info(path):
  file_name = os.path.basename(path)
  print(file_name)

  creation_timestamp = subprocess.check_output(["stat", "-f", "%B", path]).decode().strip()
  creation_time = datetime.fromtimestamp(int(creation_timestamp)).strftime("%H:%M   %d/%m/%Y")
  print(creation_time)

  update_time = datetime.fromtimestamp(os.stat(path).st_mtime).strftime("%H:%M   %d/%m/%Y")
  print(update_time)

  git_url = subprocess.check_output(["git", "remote", "get-url", "origin"], cwd=os.path.dirname(path)).decode().strip()
  if git_url.startswith("https://"):
    git_user = git_url.split("/")[-2]
    git_repo = git_url.split("/")[-1].replace(".git", "")
  elif git_url.startswith("git@"):
    git_user = git_url.split(":")[1].split("/")[-1]
    git_repo = git_url.split(":")[1].split("/")[-1].replace(".git", "")
  else:
    git_user = "unknown"
    git_repo = "unknown"
  print(git_repo)
  print(git_user)

  rel_path = os.path.relpath(path, git_repo)
  print(rel_path)

path = os.path.expanduser("~/Desktop/Projects/ascii2header/header_example.txt")
get_info(path)