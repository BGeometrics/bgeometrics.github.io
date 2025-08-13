#!/usr/bin/python3

"""
Script para generar las páginas dark
"""

import os
import shutil
import re

def create_directory_if_not_exists(directory):
    os.makedirs(directory, exist_ok=True)
    print(f"Directory created or already exists: {directory}")

def remove_all_files(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Construct full file path
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
            else:
                print(f"Skipped: {file_path} (not a file)")
        except Exception as e:
            print(f"Failed to remove {file_path}: {e}")

def copy_files(src_dir, dest_dir):
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    # Iterate over all files in the source directory
    for filename in os.listdir(src_dir):
        # Construct full file path
        src_file_path = os.path.join(src_dir, filename)
        
        # Check if it is a file (not a directory)
        if os.path.isfile(src_file_path):
            dest_file_path = os.path.join(dest_dir, filename)
            # Copy the file to the destination directory
            shutil.copy2(src_file_path, dest_file_path)
            print(f"Copied: {src_file_path} to {dest_file_path}")

def copy_files_excluding_word(src_dir, dest_dir, exclude_word):
    os.makedirs(dest_dir, exist_ok=True)
    
    for filename in os.listdir(src_dir):
        # Check if the file contains the excluded word
        if exclude_word not in filename:
            # Construct full file path
            src_file = os.path.join(src_dir, filename)
            dest_file = os.path.join(dest_dir, filename)
            # Copy file to the destination directory
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {src_file} to {dest_file}")

def rename_files_in_directory(directory, word_to_add, position='prefix'):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # Split the filename and its extension
            name, ext = os.path.splitext(filename)
            
            # Add the word to the filename
            if position == 'prefix':
                new_name = f"{word_to_add}_{name}{ext}"
            elif position == 'suffix':
                new_name = f"{name}_{word_to_add}{ext}"
            else:
                raise ValueError("position argument must be 'prefix' or 'suffix'")
            
            new_file_path = os.path.join(directory, new_name)
            
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_path} to {new_file_path}")

def remove_extension_from_files(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # Split the filename and its extension
            name, ext = os.path.splitext(filename)
            
            # Check if there is an extension to remove
            if ext:
                new_name = name  # The new name is the filename without the extension
                new_file_path = os.path.join(directory, new_name)
                
                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_path} to {new_file_path}")

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

def search_replace_dark(_file, _file_out, _search, _replace):

    with open(_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace(_search, _replace)

    with open(_file_out, 'w') as file:
        file.write(filedata)

    file.close()

    return _file_out


src_directory = '/home/pi/bgeometrics.github.io/graphics'
dest_directory = '/tmp/graphics'
word_to_exclude = 'dark'

create_directory_if_not_exists(dest_directory)

remove_all_files(dest_directory)
copy_files_excluding_word(src_directory, dest_directory, word_to_exclude)
remove_extension_from_files(dest_directory)

word_to_add = 'dark.html'
position = 'suffix'  
rename_files_in_directory(dest_directory, word_to_add, position)

file_extension = '.html'
old_text = """color: 'black'"""
new_text = """color: 'white'"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

file_extension = '.html'
old_text = """color: 'rgba(0, 0, 0, 1)'"""
new_text = """color: 'white'"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

old_text = """BGeometrics_logo.png"""
new_text = """BGeometrics_logo_write.png"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

old_text="""
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
"""
new_text = """
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
    <script src="https://code.highcharts.com/themes/brand-dark.js"></script>
    <style>
        :root {
            --highcharts-neutral-color-3: #000000;
        }

        .highcharts-contextbutton .highcharts-button-symbol {
            stroke: #000000 !important; 
            fill: #000000 !important; 
        }

        .highcharts-menu-item { 
            background-color: #000000 !important; 
            color: #FFFFFF !important; 
        }   

        .highcharts-menu {
            background-color: #000000 !important; 
            border: 1px solid #ccc !important;
            color: #dddddd !important; 
        }
    </style>
"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

old_text="""events: {
"""
new_text = """backgroundColor: 'black',
                events: {
"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)


old_text=""", opacity: 0.1}"""
new_text=""", opacity: 0.3}"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

old_text="""type: 'heatmap',"""
new_text = """type: 'heatmap', backgroundColor: '#000000',""" 
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

old_text = """fontSize: '14px'"""
new_text = """fontSize: '14px', color: '#FFFFFF',"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

# Remove grid
old_text = """title: {
                    text: 'BTC price'
                },"""
new_text = """title: {
                    text: 'BTC price'
                },
                gridLineWidth: 0,
                """
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

old_text = """yAxis: [{"""
new_text = """yAxis: [{
                gridLineWidth: 0,"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

# Copy files mode light to dark because these pages no visual good in dark


copy_files(dest_directory, src_directory)

