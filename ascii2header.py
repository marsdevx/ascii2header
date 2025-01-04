import os
import sys
import math
import random
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

def generate_header_core(info, ascii):

  width = 115
  header_lines = []
  ascii_index = 0

  with open(ascii, 'r', encoding='utf-8') as file:
    ascii = file.readlines()

  ascii_lines = len(ascii)
  if ascii_lines < 9:
    print("Usage: ASCII art must be at least 9 lines")
    sys.exit(1)

  start_point = math.floor((ascii_lines - 9) / 2)
  
  for i in range(ascii_lines):
    if i >= start_point and i < start_point + len(info):
      info_key = list(info.keys())[ascii_index]
      info_value = info[info_key]
      info_line = info_value.ljust(width // 2)
      art_line = ascii[i].strip() if i < len(ascii) else ''
      combined_line = f"{info_line}{art_line.rjust(width - len(info_line))}"
      header_lines.append(combined_line)
      ascii_index += 1
    else:
      art_line = ascii[i].strip()
      empty_info = ' ' * (width // 2)
      combined_line = f"{empty_info}{art_line.rjust(width - len(empty_info))}"
      header_lines.append(combined_line)

  return '\n'.join(header_lines)

def gen_header(path, header_core, info):

  _, file_ext = os.path.splitext(info['file_name'])

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
  if len(sys.argv) < 2:
    print("Usage: ascii2header <file> <ascii_art>")
    sys.exit(1)
  if len(sys.argv) == 2:
    ascii_arts_dir = os.path.expanduser("~/Desktop/Projects/ascii2header/ascii-arts")
    ascii_files = [f for f in os.listdir(ascii_arts_dir) if os.path.isfile(os.path.join(ascii_arts_dir, f))]
    ascii = random.choice(ascii_files)
  if len(sys.argv) == 3:
    ascii = sys.argv[2]
    
  ascii = os.path.expanduser(f"~/Desktop/Projects/ascii2header/ascii-arts/{ascii}")
  if not os.path.exists(ascii):
    print(f"Error: The file '{ascii}' does not exist.")
    sys.exit(1)
  
  path = os.path.abspath(os.path.expanduser(sys.argv[1]))
  if not os.path.exists(path):
    print(f"Error: The file '{path}' does not exist.")
    sys.exit(1)

  info = header_info(path)
  header_core = generate_header_core(info, ascii)
  header = gen_header(path, header_core, info)


  with open(path, "r") as file:
    existing_content = file.readlines()

  lines_to_skip = 0
  for line in existing_content:
    if line.strip().startswith(("/*", "#")):
      lines_to_skip += 1
    else:
      break

  if lines_to_skip > 0:
    existing_content = existing_content[lines_to_skip:]
  
  if len(existing_content) < 2 or existing_content[0].strip() or existing_content[1].strip():
    existing_content = ["\n", "\n"] + existing_content

  with open(path, "w") as file:
    file.write(header)
    file.writelines(existing_content)

if __name__ == "__main__":
  write_header()