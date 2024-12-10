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
#old_text = """<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Nunito:300,300i,400,400i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">"""

#new_text = """<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Nunito:300,300i,400,400i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" media="print" onload="this.onload=null;this.removeAttribute('media');" fetchpriority="high">"""


def search_text_in_directory(directory, search_text, file_extension=None):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path) and (file_extension is None or filename.endswith(file_extension)):
            with open(file_path, 'r', encoding='utf-8') as file:

                for line_number, line in enumerate(file, start=1):
                    if search_text in line:
                        print(f"{file_path}")
                        #results.append((file_path, line_number, line.strip()))


file_extension = '.html'  
directory_path = '/home/pi/bgeometrics.github.io/alfabitcoin'
old_text = """                        chart1.stockTools.showhideBtn.click();"""
new_text = """"""

#search_text_in_directory(directory_path, old_text, file_extension)
replace_text_in_directory(directory_path, old_text, new_text, file_extension)

