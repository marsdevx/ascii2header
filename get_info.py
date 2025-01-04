import os
import subprocess
from datetime import datetime

def get_info(path):
  info = {
    "file_name": "",
    "git_repo": "",
    "git_user": "",
    "creation_time": "",
    "update_time": "",
    "rel_path": ""
  }
  file_name = os.path.basename(path)
  info['file_name'] = file_name

  creation_timestamp = subprocess.check_output(["stat", "-f", "%B", path]).decode().strip()
  creation_time = datetime.fromtimestamp(int(creation_timestamp)).strftime("%H:%M   %d/%m/%Y")
  info['creation_time'] = creation_time

  update_time = datetime.fromtimestamp(os.stat(path).st_mtime).strftime("%H:%M   %d/%m/%Y")
  info['update_time'] = update_time

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

  info['git_user'] = git_user
  info['git_repo'] = git_repo


  rel_path = os.path.relpath(path, git_repo)[1:]
  info['rel_path'] = rel_path
  
  return info

path = os.path.expanduser("~/Desktop/Projects/ascii2header/header_example.txt")
print(get_info(path))