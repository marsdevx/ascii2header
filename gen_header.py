import os
import get_info

def generate_header(info, ascii_art_path):

  width = 115
  header_lines = []
  ascii_index = 0

  with open(ascii_art_path, 'r', encoding='utf-8') as file:
    ascii_art_path = file.readlines()
  
  for key, value in info.items():
    info_line = value.ljust(width // 2) 
    art_line = ascii_art_path[ascii_index].strip() if ascii_index < len(ascii_art_path) else ''
    combined_line = f"{info_line}{art_line.rjust(width - len(info_line))}"  
    header_lines.append(combined_line)
    ascii_index += 1

  while ascii_index < len(ascii_art_path):
    art_line = ascii_art_path[ascii_index].strip()
    empty_info = ' ' * (width // 2)
    combined_line = f"{empty_info}{art_line.rjust(width - len(empty_info))}"
    header_lines.append(combined_line)
    ascii_index += 1

  return '\n'.join(header_lines)



file_path = os.path.expanduser("~/Desktop/Projects/ascii2header/header_example.txt")
ascii_art_path = os.path.expanduser("~/Desktop/Projects/ascii2header/anime_girl.txt")
info = get_info.header_info(file_path)

header = generate_header(info, ascii_art_path)
output_file = "generated_header.txt"
with open(output_file, "w", encoding="utf-8") as file:
  file.write(header)