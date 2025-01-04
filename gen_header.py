import os
import gen_header_txt
import get_info

def gen_header(header_core, file_ext):
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





file_path = os.path.expanduser("~/Desktop/Projects/ascii2header/header_example.txt")
ascii_art_path = os.path.expanduser("~/Desktop/Projects/ascii2header/anime_girl.txt")
info = get_info.header_info(file_path)

_, file_ext = os.path.splitext(info['file_name'])
header_core = gen_header_txt.generate_header_core(info, ascii_art_path)

header = gen_header(header_core, file_ext)

output_file = "generated_header.txt"
with open(output_file, "w", encoding="utf-8") as file:
  file.write(header)