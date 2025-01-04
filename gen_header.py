import os
import gen_header_txt
import get_info

file_path = os.path.expanduser("~/Desktop/Projects/ascii2header/header_example.txt")
ascii_art_path = os.path.expanduser("~/Desktop/Projects/ascii2header/anime_girl.txt")
info = get_info.header_info(file_path)

header = gen_header_txt.generate_header_core(info, ascii_art_path)
output_file = "generated_header.txt"
with open(output_file, "w", encoding="utf-8") as file:
  file.write(header)