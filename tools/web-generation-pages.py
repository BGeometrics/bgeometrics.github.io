#!/usr/bin/python3

"""
Script para generar las páginas web con el menú.
Pasos:
- Se crea la página con el gráfico
- Se añade la opción de menú en el fichero web-generation-model.html
- Se añade en el fichero web-generation-pages-all.txt con estos campos
file_name,file_end,title,iframe_html,description,keywords
- Si tiene texto explicativo se añade en el fichero web-generation-*-end-* están la parte html del final de cada páginas/s 
- Se ejecuta este script web-generation-pages-all.py en ~/bgeometrics.github.io/tools/

Para copiar al proyecto las páginas generadas
cp /tmp/web/* /home/pi/bgeometrics.github.io/

Para llevarlas a local,
scp pi@192.168.1.66:/tmp/web/* .

Por último hay que subirlas a github
git add *
...

"""

import os


def concatenate_files(file1_path, file2_path, output_file_path):
    try:
        with open(file1_path, 'r') as file1:
            content1 = file1.read()

        with open(file2_path, 'r') as file2:
            content2 = file2.read()

        concatenated_content = content1 + content2

        with open(output_file_path, 'w') as output_file:
            output_file.write(concatenated_content)

        print(f"Files '{file1_path}' and '{file2_path}' have been successfully concatenated to '{output_file_path}'.")
    except Exception as e:
        print(f"Error: {e}")


def remove_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)

        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File '{file_path}' has been removed.")

        print(f"All files in the directory '{directory_path}' have been successfully removed.")
    except Exception as e:
        print(f"Error: {e}")

# Remove files directory
directory_path = '/tmp/web'
remove_files_in_directory(directory_path)

# Remove files directory
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-charts-end.html'
output_file_path = 'web-generation-model-out.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate charts pages
file_name = 'web-generation-pages.txt'
file_model = output_file_path 
checkWords = ("__title__","__description__","__keywords__", "__iframe__")

with open(file_name, 'r') as archive:
    next(archive)

    for line in archive:
        line = line.strip()
        fields = line.split(',')
        #print(fields)

        file_out = fields[0]
        file_end = fields[1]
        title = fields[2]
        iframe = fields[3]
        description = fields[4]
        #keywords = fields[5]
        keywords = title

        print(file_out)

        repWords = (title,description,keywords,iframe)

        f_model = open(file_model, 'r')
        f_out = open(file_out, 'w')
        
        for line in f_model:
            for check, rep in zip(checkWords, repWords):
                line = line.replace(check, rep)
            f_out.write(line)

        with open(file_end) as fp:
            f_end = fp.read()

        f_out.write(f_end)
        f_out.close()
        f_model.close()


# Generate index.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-index-end.html'
output_file_path = '/tmp/web/index.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Only generate new pages in web-generation-pages.txt
"""
# Generate page services.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-services-end.html'
output_file_path = '/tmp/web/services.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate page contact.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-contact-end.html'
output_file_path = '/tmp/web/pages-contact.html'

concatenate_files(file1_path, file2_path, output_file_path)
"""
