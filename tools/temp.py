#!/usr/bin/python3

"""
Script para generar las páginas web con el menú.
Pasos:
- Se crea las páginas, modo light y modo dark, con el gráfico
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

# Se modifica el fichero general de los menús (web-generation-model.html) para adaptarlo al modo dark
def search_replace_dark(_file, _file_out):

    with open(_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('>Light<', '>Dark<')
    filedata = filedata.replace('fa-flag-usa" aria-hidden="true"></i> Light', 'fa-flag-usa" aria-hidden="true"></i> Dark')
    filedata = filedata.replace('fa-flag-es" aria-hidden="true"></i> Dark', 'fa-flag-es" aria-hidden="true"></i> Light')
    filedata = filedata.replace('.html', '_dark.html')
    filedata = filedata.replace('index_dark_dark.html', 'index.html')
    filedata = filedata.replace('swagger-ui/index_dark.html', 'swagger-ui/index.html')
    filedata = filedata.replace('css/style.css', 'css/style-dark.css')

    with open(_file_out, 'w') as file:
        file.write(filedata)
    
    file.close()

    return _file_out

"""
def search_replace_index_dark(_file):
    _file_out = 'web-generation-model-index-end-dark.html'

    with open(_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('.html', '_dark.html')

    with open(_file_out, 'w') as file:
        file.write(filedata)
    
    file.close()

    return _file_out
"""

# Generate charts pages
def generate_pages(_mode):
    file_name = 'web-generation-pages-all.txt'
    file_model = output_file_path 
    checkWords = ("__title__","__description__","__keywords__", "__iframe__")

    with open(file_name, 'r') as archive:
        next(archive)

        menu = ''
        file_out = ''

        #file_name,text file_end,title,iframe_html,description,keywords,file_model,group_menu
        for line in archive:
            line = line.strip()
            fields = line.split(',')
            file_out = fields[0]    # Nombre del fichero final
            file_end = fields[1]    # Nombre del fichero que se va a concatenar al final
            title = fields[2]       # Título
            iframe = fields[3]      # URL del gráfico que se añade al iframe 
            keywords = fields[4]    # Palabras claves de la página, es para los buscadores
            description = fields[5] # Descripción de la página. No lo estoy utilizando
            menu = fields[6]        # Grupo de menú en el que se encuentra
            
            # Reprocesamos los campos que hay que cambiar por el modo oscuro
            if _mode == 'dark':
                file_out = fields[0].replace(".html", "_dark.html")
                print(file_out)

                if fields[3].find('reports') == -1 and fields[3].find('montecarlo') == -1:
                    iframe = fields[3].replace(".html", "_dark.html")
                #else:
                #    print("")
                #    print(file_out)
                #    print("A estas páginas no se le añade el dark")
                #    print(iframe)

            repWords = (title,description,keywords,iframe)

            f_model = open(file_model, 'r')
            f_out = open(file_out, 'w')
            
            # Textos a buscar para remplazar y que se muestren los menús desplegados y activos
            menu_file = '<ul id="' + menu + '" class="nav-content collapse"'
            pos = file_out.rfind('/')
            file_name = file_out[pos+1:]
            file_link = '<a href="' + file_name + '"'

            for line in f_model:
                for check, rep in zip(checkWords, repWords):
                    line = line.replace(check, rep)

                # Para que el grupo de menu de la gráfica aparezca desplegado
                if line.find(menu_file) != -1:
                    line = line.replace('nav-content collapse', 'nav-content')

                # Para que la opción de menú se vea activa
                if line.find(file_link) != -1:
                    line = line.replace(file_link, file_link + ' class="active"')

                f_out.write(line)

            with open(file_end) as fp:
                f_end = fp.read()

            f_out.write(f_end)
            f_out.close()
            f_model.close()


# Asegurarse que existe el directorio
directory_path = '/tmp/web'
directory_path_es = '/tmp/web/es'


# Generate page workspace.html with menu
with open('web-generation-model.html', 'r') as file:
  filedata = file.read()

filedata = filedata.replace("""<body>""", """<body onload="init()">
  <link rel="stylesheet" type="text/css" href="https://code.highcharts.com/css/stocktools/gui.css">
  <link rel="stylesheet" type="text/css" href="https://code.highcharts.com/css/annotations/popup.css">

  <script src="https://code.highcharts.com/stock/highstock.js"></script>
  <script src="https://code.highcharts.com/stock/indicators/indicators-all.js"></script>
  <script src="https://code.highcharts.com/stock/modules/drag-panes.js"></script>
  <script src="https://code.highcharts.com/modules/annotations-advanced.js"></script>
  <script src="https://code.highcharts.com/modules/price-indicator.js"></script>
  <script src="https://code.highcharts.com/modules/full-screen.js"></script>
  <script src="https://code.highcharts.com/modules/stock-tools.js"></script>
  <script src="https://code.highcharts.com/stock/modules/heikinashi.js"></script>
  <script src="https://code.highcharts.com/modules/accessibility.js"></script>
  <script src="https://charts.bgeometrics.com/assets/js/bgeometrics.js"></script>""")
filedata = filedata.replace('<title>BGeometrics</title>', '<title>BGeometrics Workspace Charts</title>')

with open('web-generation-model-workspace.html', 'w') as file:
  file.write(filedata)

file1_path = 'web-generation-workspace-menu.html'
file2_path = 'workspace_dashboard.html'
output_file_path = 'web-generation-model-workspace-2.html'
concatenate_files(file1_path, file2_path, output_file_path)

file1_path = 'web-generation-model-workspace.html'
file2_path = 'web-generation-model-workspace-2.html'
output_file_path = '/tmp/workspace_dashboard.html'
concatenate_files(file1_path, file2_path, output_file_path)
