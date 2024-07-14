import os
import re

def replace_text_in_directory(directory, old_text, new_text, file_extension=None):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path) and (file_extension is None or filename.endswith(file_extension)):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            modified_content = re.sub(re.escape(old_text), new_text, content)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
                
            print(f"Processed file: {file_path}")

# Usage
directory_path = '/home/pi/bgeometrics.github.io/tools/es'
#old_text = """<link href="assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/quill/quill.snow.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/quill/quill.bubble.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/remixicon/remixicon.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/simple-datatables/style.css" rel="stylesheet">"""
#old_text = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZR3ZFTF2FK"></script>"""
new_text = """"""
file_extension = '.html'  

replace_text_in_directory(directory_path, old_text, new_text, file_extension)

