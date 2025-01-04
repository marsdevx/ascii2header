import os
import get_info

path = os.path.expanduser("~/Desktop/Projects/ascii2header/header_example.txt")
print(get_info.header_info(path))