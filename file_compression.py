from typing import List
import zipfile
import os

def compress_files(output_zip: str, files: List[str]):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            if os.path.isfile(file):
                zipf.write(file, os.path.basename(file))
            elif os.path.isdir(file):
                for root, _, filenames in os.walk(file):
                    for filename in filenames:
                        filepath = os.path.join(root, filename)
                        zipf.write(filepath, os.path.relpath(filepath, file))
