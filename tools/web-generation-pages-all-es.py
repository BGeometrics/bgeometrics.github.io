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

- Añadir las páginas en español
...

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
import re


lang = "es"

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

    filedata = filedata.replace('>Claro<', '>Oscuro<')
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


# Generate charts pages
def generate_pages(_mode):
    replace_ini = "/tmp/web/"
    replace_end = "/tmp/web/" + lang + "/"
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
            #file_out = fields[0]    # Nombre del fichero final
            file_out = fields[0].replace(replace_ini, replace_end) # Nombre con el directorio del idioma
            file_end = lang + '/' + fields[1]    # Nombre del fichero que se va a concatenar al final
            title = fields[2]       # Título
            #iframe = lang + '/' + fields[3]      # URL del gráfico que se añade al iframe 
            iframe = fields[3]      # URL del gráfico que se añade al iframe 
            keywords = fields[4]    # Palabras claves de la página, es para los buscadores
            description = fields[5] # Descripción de la página. No lo estoy utilizando
            menu = fields[6]        # Grupo de menú en el que se encuentra
            
            # Reprocesamos los campos que hay que cambiar por el modo oscuro
            if _mode == 'dark':
                file_out = file_out.replace(".html", "_dark.html")

                if fields[3].find('reports') == -1 and fields[3].find('montecarlo') == -1:
                    iframe = fields[3].replace(".html", "_dark.html")
                #else:
                #    print("")
                #    print(file_out)
                #    print("A estas páginas no se le añade el dark")
                #    print(iframe)

            print(file_out)
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
directory_path_es = '/tmp/web/' + lang

if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print("Directory created successfully!")

if not os.path.exists(directory_path_es):
    os.makedirs(directory_path_es)
    print("Directory es created successfully!")

# Remove files directory
remove_files_in_directory(directory_path_es)

file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-charts-end.html'
output_file_path = lang + '/web-generation-model-out.html'

try:
    concatenate_files(file1_path, file2_path, output_file_path)
    generate_pages('light')
except Exception as e:
    print(f"Error: {e}")

# Generate index.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-index-end.html'
output_file_path = '/tmp/web/' + lang + '/index.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_6m.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-end-index-6m.html'
output_file_path = '/tmp/web/' + lang + '/index_6m.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_3m.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-end-index-3m.html'
output_file_path = '/tmp/web/' + lang + '/index_3m.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate page workspace.html with menu
with open(lang + '/web-generation-model.html', 'r') as file:
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

with open(lang + '/web-generation-model-workspace.html', 'w') as file:
  file.write(filedata)

#TODO: Traducir y copiar en lang + '/...'
file1_path = 'web-generation-workspace-menu.html'
file2_path = 'web-generation-workspace-3.html'
output_file_path = lang + '/web-generation-workspace-2.html'
concatenate_files(file1_path, file2_path, output_file_path)

file1_path = lang + '/web-generation-model-workspace.html'
file2_path = lang + '/web-generation-workspace-2.html'
output_file_path = '/tmp/web/' + lang + '/workspace.html'
concatenate_files(file1_path, file2_path, output_file_path)


# Generate page services.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-services-end.html'
output_file_path = '/tmp/web/' + lang + '/services.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page contact.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-contact-end.html'
output_file_path = '/tmp/web/' + lang + '/pages-contact.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page donation.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-donation-end.html'
output_file_path = '/tmp/web/' + lang + '/donation.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page api.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-bitcoin-api-end.html'
output_file_path = '/tmp/web/' + lang + '/bitcoin_api.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page ohlc_dashboard.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-ohlc-dashboards-end.html'
output_file_path = '/tmp/web/' + lang + '/ohlc_dashboard.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page miner_dsahboard.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-miner-end.html'
output_file_path = '/tmp/web/' + lang + '/miner_dashboard.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_trend.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-dashboard-trend-end.html'
output_file_path = '/tmp/web/' + lang + '/dashboard_trend.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_market_peaks.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-dashboard-market-peaks-end.html'
output_file_path = '/tmp/web/' + lang + '/dashboard_market_peaks.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_short_term_trend.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-dashboard-short-term-trend-end.html'
output_file_path = '/tmp/web/' + lang + '/dashboard_short_term_trend.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_demand.html with menu
file1_path = lang + '/web-generation-model.html'
file2_path = lang + '/web-generation-model-dashboard-demand-end.html'
output_file_path = '/tmp/web/' + lang + '/dashboard_demand.html'
concatenate_files(file1_path, file2_path, output_file_path)



### Mode dark 

_file_out = lang + '/web-generation-model-dark.html' 
file_out_dark = search_replace_dark(file1_path, _file_out)
#file_model_index_dark = search_replace_index_dark('web-generation-model-index-end.html')
file2_path = lang + '/web-generation-model-charts-end.html'
output_file_path = lang + '/web-generation-model-out-dark.html'
print(output_file_path)

concatenate_files(file_out_dark, file2_path, output_file_path)

try:
    generate_pages('dark')
except Exception as e:
    print(f"Error: {e}")

# Generate index.html with menu dark
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-index-end-dark.html'
output_file_path = '/tmp/web/' + lang + '/index_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_6m.html with menu dark
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-end-index-6m-dark.html'
output_file_path = '/tmp/web/' + lang + '/index_6m_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_3m.html with menu dark
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-end-index-3m-dark.html'
output_file_path = '/tmp/web/' + lang + '/index_3m_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page workspace.html with menu dark
with open(lang + '/web-generation-model-dark.html', 'r') as file:
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
  <script src="https://charts.bgeometrics.com/assets/js/bgeometrics.js"></script>

  <script src="https://code.highcharts.com/themes/brand-dark.js"></script>""")

# If necesary for some cases
filedata = filedata.replace("""<body onload="init()">""", """<body onload="init()">
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
  <script src="https://charts.bgeometrics.com/assets/js/bgeometrics.js"></script>

  <script src="https://code.highcharts.com/themes/brand-dark.js"></script>""")

filedata = filedata.replace('<title>BGeometrics</title>', '<title>BGeometrics Workspace Charts</title>')

with open(lang + '/web-generation-model-workspace-dark.html', 'w') as file:
  file.write(filedata)

#TODO: Traducir y copiar en lang + '/...'
file1_path = 'web-generation-workspace-menu.html'
file2_path = 'web-generation-workspace-3-dark.html'
output_file_path = lang + '/web-generation-workspace-2-dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

file1_path = lang + '/web-generation-model-workspace-dark.html'
file2_path = lang + '/web-generation-workspace-2-dark.html'
output_file_path = '/tmp/web/' + lang + '/workspace_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)


# Generate page services.html with menu dark
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-services-end.html'
output_file_path = '/tmp/web/' + lang + '/services_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page contact.html with menu dark
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-contact-end.html'
output_file_path = '/tmp/web/' + lang + '/pages-contact_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page donation.html with menu dark
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-donation-end.html'
output_file_path = '/tmp/web/' + lang + '/donation_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page ohlc_dashboard.html with menu
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-ohlc-dashboards-end.html'
output_file_path = '/tmp/web/' + lang + '/ohlc_dashboard_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page miner_dsahboard.html with menu
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-miner-end.html'
output_file_path = '/tmp/web/' + lang + '/miner_dashboard_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_trend.html with menu
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-dashboard-trend-end.html'
output_file_path = '/tmp/web/' + lang + '/dashboard_trend_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_market_peaks.html with menu
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-dashboard-market-peaks-end.html'
output_file_path = '/tmp/web/' + lang + '/dashboard_market_peaks_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_short_term_trend.html with menu
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-dashboard-short-term-trend-end.html'
output_file_path = '/tmp/web/' + lang + '/dashboard_short_term_trend_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_demand.html with menu
file1_path = lang + '/web-generation-model-dark.html'
file2_path = lang + '/web-generation-model-dashboard-demand-end.html'
output_file_path = '/tmp/web/' + lang + '/dashboard_demand_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Replace doble main by main
dest_directory = '/home/pi/bgeometrics.github.io/' + lang + '/'
file_extension = '.html'

old_text = """
  <main id="main" class="main">
  <main id="main" class="main">
"""
new_text = """
  <main id="main" class="main">
"""
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=file_extension)
dest_directory = '/tmp/web/' + lang + '/'
replace_text_in_directory(dest_directory, old_text, new_text, file_extension=file_extension)


print("")
print("For copy generate pages to project") 
print("cp /tmp/web/* /home/pi/bgeometrics.github.io/")
print("cd ..")
print("git commit -a -m... ")
print("git push")
print("")

