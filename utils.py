import os

key = f"-{os.urandom(4).hex()}"
root_path = os.path.abspath(os.path.dirname(__file__))
# export_path = os.path.join(root_path, f"export{key}.txt")
export_path = os.path.join(root_path, f"export.txt")
