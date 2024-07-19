#!/usr/bin/python3

"""
Script gor generation the dark pages
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


src_directory = '/home/pi/bgeometrics.github.io/graphics'
dest_directory = '/tmp/graphics'
word_to_exclude = 'dark'

create_directory_if_not_exists(dest_directory)

# Lang ES
src_directory = '/home/pi/bgeometrics.github.io/es/graphics'
dest_directory = '/tmp/graphics'
word_to_exclude = 'dark'

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

old_text = """BGeometrics_logo.png"""
new_text = """BGeometrics_logo_write.png"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

old_text="""
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
"""
new_text = """
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
    <script src="https://charts.bgeometrics.com/assets/js/themes/brand-dark.js"></script>
"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=None)

copy_files(dest_directory, src_directory)


