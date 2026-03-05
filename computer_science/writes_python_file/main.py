#generate a python file named clone.py that prints "new program"

from pathlib import Path


file_path = Path("clone.py")
with open(file_path, "w") as file:
    file.write("print(\"new program\")\n")