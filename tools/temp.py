#!/usr/bin/python3


def search_replace(_file, _file_out, _text_ori, _text_end):

    with open(_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace(_text_ori, _text_end)

    with open(_file_out, 'w') as file:
        file.write(filedata)

    file.close()

    return _file_out


file_data = '../files/glm2.json'
with open(file_data, 'r') as file:
    file_content = file.read()

file_in = '../graphics/m2_global_data.html'
file_out = '/tmp/m2_global_data.html'
text_ori = 'AAA'
text_end = file_content
search_replace(file_in, file_out, text_ori, text_end)

file_data = '../files/m2_yoy_change.json'
with open(file_data, 'r') as file:
    file_content = file.read()

file_in = file_out
text_ori = 'BBB'
text_end = file_content
search_replace(file_in, file_out, text_ori, text_end)

file_data = '../files/m2_weeks7_change.json'
with open(file_data, 'r') as file:
    file_content = file.read()

file_in = file_out
text_ori = 'CCC'
text_end = file_content
search_replace(file_in, file_out, text_ori, text_end)

