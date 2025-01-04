import os
import math
import get_info

def generate_header(info, ascii_art_path):

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



file_path = os.path.expanduser("~/Desktop/Projects/ascii2header/header_example.txt")
ascii_art_path = os.path.expanduser("~/Desktop/Projects/ascii2header/anime_girl.txt")
info = get_info.header_info(file_path)

header = generate_header(info, ascii_art_path)
output_file = "generated_header.txt"
with open(output_file, "w", encoding="utf-8") as file:
  file.write(header)