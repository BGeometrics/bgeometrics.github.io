import os
import re

def replace_text_in_directory(directory, old_text, new_text, file_extension=None):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Construct full file path
        file_path = os.path.join(directory, filename)
        
        # Check if it's a file (not a directory) and optionally check for file extension
        if os.path.isfile(file_path) and (file_extension is None or filename.endswith(file_extension)):
            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace the old text with the new text
            modified_content = re.sub(re.escape(old_text), new_text, content)
            
            # Write the modified content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
                
            print(f"Processed file: {file_path}")

# Usage
directory_path = '/home/pi/bgeometrics.github.io/tools'
old_text = """<link href="assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/quill/quill.snow.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/quill/quill.bubble.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/remixicon/remixicon.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/simple-datatables/style.css" rel="stylesheet">"""
new_text = """"""
file_extension = '.html'  

replace_text_in_directory(directory_path, old_text, new_text, file_extension)

