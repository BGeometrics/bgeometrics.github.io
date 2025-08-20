import os
import re

def replace_text_in_directory(directory, old_text, new_text, file_extension=None):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path) and (file_extension is None or filename.endswith(file_extension)):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            modified_content = content.replace(old_text, new_text)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
                
            print(f"Processed file: {file_path}")

def search_text_in_directory(directory, search_text, file_extension=None):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path) and (file_extension is None or filename.endswith(file_extension)):
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    if search_text in line:
                        print(f"{file_path}")

def replace_text_in_directory_regex(directory, old_pattern, new_text, file_extension=None):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and (file_extension is None or filename.endswith(file_extension)):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            # Busca el patrón y reemplaza
            modified_content, count = re.subn(old_pattern, new_text, content, flags=re.DOTALL)
            if count > 0:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(modified_content)
                print(f"Reemplazado en: {file_path}")

def search_regex_in_directory(directory, pattern, file_extension=None):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and (file_extension is None or filename.endswith(file_extension)):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            if re.search(pattern, content, flags=re.DOTALL):
                print(f"Coincidencia en: {file_path}")

file_extension = '.html'  
directory_path = '../graphics'
old_text = """    <script src="https://code.highcharts.com/modules/exporting.js"></script>"""
new_text = """"""

#search_text_in_directory(directory_path, old_text, file_extension)
replace_text_in_directory(directory_path, old_text, new_text, file_extension)

# Expresión regular flexible para el bloque stockTools
#old_pattern = r"stockTools:\s*\{\s*gui:\s*\{\s*enabled:\s*false\s*\}\s*\},,"
#new_text = """stockTools: {
#                            gui: {
#                                enabled: false 
#                            }
#                        },
#                        navigator: {
#                            enabled: false 
#                        },
#                        yAxis: [{
#                            title: { text: null }
#                        }, {
#                            title: { text: null }
#                        }],"""

#replace_text_in_directory_regex(directory_path, old_pattern, new_text, file_extension)
#search_regex_in_directory(directory_path, old_pattern, file_extension)

