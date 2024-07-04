#!/usr/bin/python3

import os


def replace_multiple_in_file(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def replace_in_all_files_in_directory(directory_path, replacements):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            replace_multiple_in_file(file_path, replacements)
            print(f"Replacements done in file {file_path}")

direc = '/home/pi'
project = '/bgeometrics.github.io'
lang = 'es'
directory_path = direc + project + '/' + lang + '/graphics/'
#file_path = direc + project + '/' + lang + '/graphics/address_active.html'

replacements = {
    "Active Addresses": "Direcciones Activas",
    "BTC price": "Precio BTC",
}

replace_in_all_files_in_directory(directory_path, replacements)
print(f"Replacements done in all files in directory {directory_path}")

