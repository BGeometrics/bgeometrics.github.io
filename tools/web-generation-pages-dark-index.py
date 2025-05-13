#!/usr/bin/python3

"""
Script para generar las páginas dark
"""

import os
import shutil
import re

def search_replace_dark(_file, _file_out, _search, _replace):

    with open(_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace(_search, _replace)

    with open(_file_out, 'w') as file:
        file.write(filedata)

    file.close()

    return _file_out


# Replace index_dark.html 

src = '/home/pi/bgeometrics.github.io/index_dark.html'
old_text = """<link href="assets/css/bgeometrics.css" rel="stylesheet">"""
new_text = """<link href="assets/css/bgeometrics.css" rel="stylesheet">
  <style>
    #searchInput {
        color: #000000 !important;
    }
    
    #searchInput::placeholder {
        color: #666666;
    }
  </style>
"""

search_replace_dark(src, src, old_text, new_text)
