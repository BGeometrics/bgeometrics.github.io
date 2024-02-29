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

Esto lo hace el script web-generation-pages-all.sh
Para copiar al proyecto las páginas generadas
cp /tmp/web/* /home/pi/bgeometrics.github.io/

Para llevarlas a local,
scp pi@192.168.1.66:/tmp/web/* .

Por último hay que subirlas a github
git add *
...
"""

import os
import fileinput


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

def search_replace_dark(_file):
    _file_out = 'web-generation-model-dark.html' 

    with open(_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('.html', '_dark.html')
    filedata = filedata.replace('index_dark_dark.html', 'index_dark.html')
    filedata = filedata.replace('swagger-ui/index_dark.html', 'swagger-ui/index.html')
    filedata = filedata.replace('css/style.css', 'css/style-dark.css')
    filedata = filedata.replace('>Light<', '>Dark<')
    filedata = filedata.replace('fa-flag-usa" aria-hidden="true"></i> Light', 'fa-flag-usa" aria-hidden="true"></i> Dark')
    filedata = filedata.replace('fa-flag-es" aria-hidden="true"></i> Dark', 'fa-flag-es" aria-hidden="true"></i> Light')

    with open(_file_out, 'w') as file:
        file.write(filedata)
    
    file.close()

    return _file_out

# Generate charts pages
def generate_pages(_mode):
    file_name = 'web-generation-pages-all.txt'
    file_model = output_file_path 
    checkWords = ("__title__","__description__","__keywords__", "__iframe__")

    with open(file_name, 'r') as archive:
        next(archive)

        for line in archive:
            line = line.strip()
            fields = line.split(',')
            
            file_out = fields[0]
            file_end = fields[1]
            title = fields[2]
            iframe = fields[3]
            keywords = fields[4]
            description = fields[5]
            
            # Reprocesamos los campos que hay que cambiar
            if _mode == 'dark':
                file_out = fields[0].replace(".html", "_dark.html")

                if fields[3].find('reports') == -1:
                    iframe = fields[3].replace(".html", "_dark.html")

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


# Asegurarse que existe el directorio
directory_path = '/tmp/web'

if not os.path.exists(directory_path):
    os.makedirs(directory)
    print("Directory created successfully!")

# Remove files directory
remove_files_in_directory(directory_path)

file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-charts-end.html'
output_file_path = 'web-generation-model-out.html'

concatenate_files(file1_path, file2_path, output_file_path)
generate_pages('light')

# Dark
file_out_dark = search_replace_dark(file1_path)
print(file_out_dark)
file2_path = 'web-generation-model-charts-end.html'
output_file_path = 'web-generation-model-out-dark.html'

concatenate_files(file_out_dark, file2_path, output_file_path)
generate_pages('dark')




# Generate index.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-index-end.html'
output_file_path = '/tmp/web/index.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_6m.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-end-index-6m.html'
output_file_path = '/tmp/web/index_6m.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_3m.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-end-index-3m.html'
output_file_path = '/tmp/web/index_3m.html'

concatenate_files(file1_path, file2_path, output_file_path)

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


### Mode dark 

# Generate index.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-index-end.html'
output_file_path = '/tmp/web/index_dark.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_6m.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-end-index-6m.html'
output_file_path = '/tmp/web/index_6m_dark.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_3m.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-end-index-3m.html'
output_file_path = '/tmp/web/index_3m_dark.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate page services.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-services-end.html'
output_file_path = '/tmp/web/services_dark.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate page contact.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-contact-end.html'
output_file_path = '/tmp/web/pages-contact_dark.html'

concatenate_files(file1_path, file2_path, output_file_path)

print("")
print("For copy generate pages to project") 
print("cp /tmp/web/* /home/pi/bgeometrics.github.io/")
print("cd ..")
print("git commit -a -m... ")
print("git push")
print("")

