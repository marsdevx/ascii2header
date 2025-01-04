import os
import sys
import math
import subprocess
from datetime import datetime

def header_info(path):
  info = {
    "file_name": "",
    "empty1": "",
    "git_repo": "",
    "git_user": "",
    "empty2": "",
    "creation_time": "",
    "update_time": "",
    "empty3": "",
    "rel_path": ""
  }
  
  file_name = os.path.basename(path)
  info['file_name'] = f"File:         {file_name}"

  creation_timestamp = subprocess.check_output(["stat", "-f", "%B", path]).decode().strip()
  creation_time = datetime.fromtimestamp(int(creation_timestamp)).strftime("%H:%M   %d/%m/%Y")
  info['creation_time'] = f"Created:      {creation_time}"

  update_time = datetime.fromtimestamp(os.stat(path).st_mtime).strftime("%H:%M   %d/%m/%Y")
  info['update_time'] = f"Updated:      {update_time}"

  git_url = subprocess.check_output(["git", "remote", "get-url", "origin"], cwd=os.path.dirname(path)).decode().strip()
  if git_url.startswith("https://"):
    git_user = git_url.split("/")[-2]
    git_repo = git_url.split("/")[-1].replace(".git", "")
  else:
    git_user = "unknown"
    git_repo = "unknown"
  info['git_user'] = f"Github:       {git_user}"
  info['git_repo'] = f"Project:      {git_repo}"

  rel_path = os.path.relpath(path, git_repo)[1:]
  info['rel_path'] = f"Path:         {rel_path}"
  
  return info

def generate_header_core(info, ascii_art_path):

  width = 115
  header_lines = []
  ascii_index = 0

  with open(ascii_art_path, 'r', encoding='utf-8') as file:
    ascii_art_path = file.readlines()

  ascii_lines = len(ascii_art_path)
  start_point = math.floor((ascii_lines - 9) / 2)
  
  for i in range(ascii_lines):
    if i >= start_point and i < start_point + len(info):
      info_key = list(info.keys())[ascii_index]
      info_value = info[info_key]
      info_line = info_value.ljust(width // 2)
      art_line = ascii_art_path[i].strip() if i < len(ascii_art_path) else ''
      combined_line = f"{info_line}{art_line.rjust(width - len(info_line))}"
      header_lines.append(combined_line)
      ascii_index += 1
    else:
      art_line = ascii_art_path[i].strip()
      empty_info = ' ' * (width // 2)
      combined_line = f"{empty_info}{art_line.rjust(width - len(empty_info))}"
      header_lines.append(combined_line)

  return '\n'.join(header_lines)

def gen_header(path, ascii_name):

  info = header_info(path)
  _, file_ext = os.path.splitext(info['file_name'])

  ascii_art_path = os.path.expanduser(f"~/Desktop/Projects/ascii2header/ascii-arts/{ascii_name}")
  if not os.path.exists(ascii_art_path):
    print(f"Error: The file '{ascii_art_path}' does not exist.")
    sys.exit(1)

  header_core = generate_header_core(info, ascii_art_path)

  if file_ext in [".c", ".css", ".js", ".ino", ".h"]:
    start_marker = "/*   "
    end_marker = "  */"
  else:
    start_marker = "#    "
    end_marker = "   #"

  header_lines = header_core.splitlines()

  header = []
  for line in header_lines:
    decorated_line = f"{start_marker}{line.ljust(116)}{end_marker}"
    header.append(decorated_line)
  header = "\n".join(header)

  return header

def write_header():
  if len(sys.argv) < 3:
    print("Usage: ascii2header <file> <ascii_art>")
    sys.exit(1)
  path = path = os.path.abspath(os.path.expanduser(sys.argv[1]))
  ascii = sys.argv[2]
  header = gen_header(path, ascii)

  with open(path, "r") as file:
    existing_content = file.read()

  with open(path, "w") as file:
    file.write(header)
    file.write("\n\n")
    file.write(existing_content)

if __name__ == "__main__":
  write_header()