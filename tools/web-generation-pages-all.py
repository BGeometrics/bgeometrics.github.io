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
import shutil


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

    # For default mode dark. Combo light and dark set page index.html to index_light 
    filedata = filedata.replace('<a class="dropdown-item" href="index.html">', '<a class="dropdown-item" href="index_light.html">')

    with open(_file_out, 'w') as file:
        file.write(filedata)
    
    file.close()

    return _file_out

def search_replace_text(_file, _file_out, _search, _replace):

    with open(_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace(_search, _replace)

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

def remove_export_scripts_from_files(file_list):
    scripts_to_remove = [
        '<script src="https://code.highcharts.com/modules/exporting.js"></script>',
        '<script src="https://code.highcharts.com/modules/export-data.js"></script>'
    ]
    for file_path in file_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if not any(script in line for script in scripts_to_remove):
                    f.write(line)
        print(f"Removed export scripts from: {file_path}")


# Asegurarse que existe el directorio
directory_path = '/tmp/web'
directory_path_es = '/tmp/web/es'

if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print("Directory created successfully!")

if not os.path.exists(directory_path_es):
    os.makedirs(directory_path_es)
    print("Directory es created successfully!")

# Remove files directory
remove_files_in_directory(directory_path)

file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-charts-end.html'
output_file_path = 'web-generation-model-out.html'

concatenate_files(file1_path, file2_path, output_file_path)
generate_pages('light')

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

# Generate page workspace.html with menu
with open('web-generation-model.html', 'r') as file:
  filedata = file.read()

filedata = filedata.replace("""<body>""", """<body onload="init()">
  <link rel="stylesheet" type="text/css" href="https://code.highcharts.com/css/stocktools/gui.css">
  <link rel="stylesheet" type="text/css" href="https://code.highcharts.com/css/annotations/popup.css">

  <!--<script src="https://code.highcharts.com/stock/highstock.js"></script>-->
  <!--<script src="https://code.highcharts.com/stock/indicators/indicators-all.js"></script>-->
  <script src="https://code.highcharts.com/stock/11.4.8/highstock.js"></script>
  <script src="https://code.highcharts.com/stock/11.4.8/indicators/indicators-all.js"></script>
  <script src="https://code.highcharts.com/stock/modules/drag-panes.js"></script>
  <script src="https://code.highcharts.com/modules/annotations-advanced.js"></script>
  <script src="https://code.highcharts.com/modules/price-indicator.js"></script>
  <script src="https://code.highcharts.com/modules/full-screen.js"></script>
  <script src="https://code.highcharts.com/modules/stock-tools.js"></script>
  <script src="https://code.highcharts.com/stock/modules/heikinashi.js"></script>
  <script src="https://code.highcharts.com/modules/accessibility.js"></script>
  <script src="https://charts.bgeometrics.com/assets/js/bgeometrics.js"></script>""")
filedata = filedata.replace('<title>BGeometrics</title>', '<title>BGeometrics Workspace Charts</title>')


# Generate sytle dark graphics/m2_global_10w_300_dark.html
with open('../graphics/m2_global_10w_300_dark.html', 'r') as file:
  filedata = file.read()

filedata = filedata.replace("""<script src="https://code.highcharts.com/modules/accessibility.js"></script>""",
    """<script src="https://code.highcharts.com/modules/accessibility.js"></script>
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
        </style>""")

with open('web-generation-model-workspace.html', 'w') as file:
  file.write(filedata)

file1_path = 'web-generation-workspace-menu.html'
file2_path = 'web-generation-workspace-3.html'
output_file_path = 'web-generation-workspace-2.html'
concatenate_files(file1_path, file2_path, output_file_path)

file1_path = 'web-generation-model-workspace.html'
file2_path = 'web-generation-workspace-2.html'
output_file_path = '/tmp/web/workspace.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate grafic workspace_dashboard.html with menu data json
with open('web-generation-workspace-menu.html', 'r') as file:
  filedata = file.read()
filedata = filedata.replace("""<main id="main" class="main">""", """""")
with open('/tmp/web-generation-workspace-menu.html', 'w') as file:
  file.write(filedata)

file1_path = '/tmp/web-generation-workspace-menu.html'
file2_path = 'workspace_dashboard.html'
output_file_path = 'web-generation-model-workspace-2-dashboard.html'
concatenate_files(file1_path, file2_path, output_file_path)


# Generate page workspace_stocks.html with menu
with open('web-generation-model.html', 'r') as file:
  filedata = file.read()

filedata = filedata.replace("""<body>""", """<body>
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
filedata = filedata.replace('<title>BGeometrics</title>', '<title>BGeometrics Workspace Stocks</title>')

with open('web-generation-model-workspace-stocks.html', 'w') as file:
  file.write(filedata)

file1_path = 'web-generation-workspace-stocks-menu.html'
file2_path = 'web-generation-workspace-stocks-3.html'
output_file_path = 'web-generation-workspace-stocks-2.html'
concatenate_files(file1_path, file2_path, output_file_path)

file1_path = 'web-generation-model-workspace-stocks.html'
file2_path = 'web-generation-workspace-stocks-2.html'
output_file_path = '/tmp/web/workspace_stocks.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page workspace_crypto.html with menu
with open('web-generation-model.html', 'r') as file:
  filedata = file.read()

filedata = filedata.replace("""<body>""", """<body>
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

filedata = filedata.replace('<title>BGeometrics</title>', '<title>BGeometrics Workspace Stocks</title>')

with open('web-generation-model-workspace-crypto.html', 'w') as file:
  file.write(filedata)

file1_path = 'web-generation-workspace-crypto-menu.html'
file2_path = 'web-generation-workspace-crypto-3.html'
output_file_path = 'web-generation-workspace-crypto-2.html'
concatenate_files(file1_path, file2_path, output_file_path)

file1_path = 'web-generation-model-workspace-crypto.html'
file2_path = 'web-generation-workspace-crypto-2.html'
output_file_path = '/tmp/web/workspace_crypto.html'
concatenate_files(file1_path, file2_path, output_file_path)


# Generate grafic workspace_dashboard.html with menu data json
with open('web-generation-workspace-menu.html', 'r') as file:
  filedata = file.read()
filedata = filedata.replace("""<main id="main" class="main">""", """""")
with open('/tmp/web-generation-workspace-menu.html', 'w') as file:
  file.write(filedata)

file1_path = '/tmp/web-generation-workspace-menu.html'
file2_path = 'workspace_dashboard.html'
output_file_path = 'web-generation-model-workspace-2-dashboard.html'
concatenate_files(file1_path, file2_path, output_file_path)


file1_path = 'workspace_dashboard_init.html'
file2_path = 'web-generation-model-workspace-2-dashboard.html'
output_file_path = '../graphics/workspace_dashboard.html'
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

# Generate page donation.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-donation-end.html'
output_file_path = '/tmp/web/donation.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page api.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-bitcoin-api-end.html'
output_file_path = '/tmp/web/bitcoin_api.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page ohlc_dashboard.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-ohlc-dashboards-end.html'
output_file_path = '/tmp/web/ohlc_dashboard.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page miner_dsahboard.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-miner-end.html'
output_file_path = '/tmp/web/miner_dashboard.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_trend.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-dashboard-trend-end.html'
output_file_path = '/tmp/web/dashboard_trend.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_market_peaks.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-dashboard-market-peaks-end.html'
output_file_path = '/tmp/web/dashboard_market_peaks.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_market_floors.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-dashboard-market-floors-end.html'
output_file_path = '/tmp/web/dashboard_market_floors.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_workspace.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-dashboard-workspace-end.html'
output_file_path = '/tmp/web/dashboard_workspace.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_workspace_400.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-dashboard-workspace-400-end.html'
output_file_path = '/tmp/web/dashboard_workspace_400.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_short_term_trend.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-dashboard-short-term-trend-end.html'
output_file_path = '/tmp/web/dashboard_short_term_trend.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_demand.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-dashboard-demand-end.html'
output_file_path = '/tmp/web/dashboard_demand.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page suggestion.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-bg-suggestion-end.html'
output_file_path = '/tmp/web/bg_suggestion.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page alert.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-bg-alert-end.html'
output_file_path = '/tmp/web/bg_alert.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page alert-modal.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-bg-alert-modal-end.html'
output_file_path = '/tmp/web/bg_alert_modal.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page alert-email.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-bg-alert-email-end.html'
output_file_path = '/tmp/web/bg_alert_email.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page links.html with menu
file1_path = 'web-generation-model.html'
file2_path = 'web-generation-model-links-end.html'
output_file_path = '/tmp/web/pages-links.html'
concatenate_files(file1_path, file2_path, output_file_path)


### Mode dark 

_file_out = 'web-generation-model-dark.html' 
file_out_dark = search_replace_dark(file1_path, _file_out)

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

old_text = """handleKeyPress(event)"""
new_text = """handleKeyPressDark(event)"""
search_replace_text(file_out_dark, file_out_dark, old_text, new_text)

file_w_dark = 'web-generation-model-workspace-dark.html'
search_replace_text(file_w_dark, file_w_dark, old_text, new_text)

file2_path = 'web-generation-model-charts-end.html'
output_file_path = 'web-generation-model-out-dark.html'
print(output_file_path)

concatenate_files(file_out_dark, file2_path, output_file_path)
generate_pages('dark')


# Generate index.html with menu dark
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-index-end-dark.html'
output_file_path = '/tmp/web/index_dark.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_6m.html with menu dark
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-end-index-6m-dark.html'
output_file_path = '/tmp/web/index_6m_dark.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate index_3m.html with menu dark
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-end-index-3m-dark.html'
output_file_path = '/tmp/web/index_3m_dark.html'

concatenate_files(file1_path, file2_path, output_file_path)

# Generate page workspace.html with menu dark
with open('web-generation-model-dark.html', 'r') as file:
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
    </style>""")
filedata = filedata.replace('<title>BGeometrics</title>', '<title>BGeometrics Workspace Charts</title>')

with open('web-generation-model-workspace-dark.html', 'w') as file:
  file.write(filedata)

file1_path = 'web-generation-workspace-menu.html'
file2_path = 'web-generation-workspace-3-dark.html'
output_file_path = 'web-generation-workspace-2-dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

file1_path = 'web-generation-model-workspace-dark.html'
file2_path = 'web-generation-workspace-2-dark.html'
output_file_path = '/tmp/web/workspace_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Style dark by background
old_text = """renderTo: 'container-iframe',"""
new_text = """renderTo: 'container-iframe', backgroundColor: 'black',"""
search_replace_text(output_file_path, output_file_path, old_text, new_text)

# Generate graphic workspace_dashboard_dark.html with menu data json
with open('web-generation-workspace-menu.html', 'r') as file:
  filedata = file.read()
filedata = filedata.replace("""<main id="main" class="main">""", """""")
with open('/tmp/web-generation-workspace-menu.html', 'w') as file:
  file.write(filedata)

file1_path = '/tmp/web-generation-workspace-menu.html'
file2_path = 'workspace_dashboard-dark.html'
output_file_path = 'web-generation-model-workspace-2-dashboard-dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

file1_path = 'workspace_dashboard_init_dark.html'
file2_path = 'web-generation-model-workspace-2-dashboard-dark.html'
output_file_path = '../graphics/workspace_dashboard_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page services.html with menu dark
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-services-end.html'
output_file_path = '/tmp/web/services_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page contact.html with menu dark
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-contact-end.html'
output_file_path = '/tmp/web/pages-contact_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page donation.html with menu dark
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-donation-end.html'
output_file_path = '/tmp/web/donation_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page api.html with menu dark
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-bitcoin-api-end.html'
output_file_path = '/tmp/web/bitcoin_api_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page ohlc_dashboard.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-ohlc-dashboards-end-dark.html'
output_file_path = '/tmp/web/ohlc_dashboard_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page miner_dsahboard.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-miner-end.html'
output_file_path = '/tmp/web/miner_dashboard_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_trend.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-dashboard-trend-end.html'
output_file_path = '/tmp/web/dashboard_trend_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_market_peaks.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-dashboard-market-peaks-end-dark.html'
output_file_path = '/tmp/web/dashboard_market_peaks_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_market_floors.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-dashboard-market-floors-end-dark.html'
output_file_path = '/tmp/web/dashboard_market_floors_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_workspace.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-dashboard-workspace-end-dark.html'
output_file_path = '/tmp/web/dashboard_workspace_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_workspace_400.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-dashboard-workspace-400-end-dark.html'
output_file_path = '/tmp/web/dashboard_workspace_400_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_short_term_trend.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-dashboard-short-term-trend-end-dark.html'
output_file_path = '/tmp/web/dashboard_short_term_trend_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page dashboard_demand.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-dashboard-demand-end-dark.html'
output_file_path = '/tmp/web/dashboard_demand_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page suggestion.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-bg-suggestion-end.html'
output_file_path = '/tmp/web/bg_suggestion_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page alert.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-bg-alert-end.html'
output_file_path = '/tmp/web/bg_alert_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page alert-modal.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-bg-alert-modal-end.html'
output_file_path = '/tmp/web/bg_alert_modal_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page alert-email.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-bg-alert-email-end.html'
output_file_path = '/tmp/web/bg_alert_email_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Generate page links.html with menu
file1_path = 'web-generation-model-dark.html'
file2_path = 'web-generation-model-links-end.html'
output_file_path = '/tmp/web/pages-links_dark.html'
concatenate_files(file1_path, file2_path, output_file_path)

# Copy workspace_stocks in dark, but no it has style dark
archivo_origen = '/home/pi/bgeometrics.github.io/workspace_stocks.html'
archivo_destino = '/tmp/web/workspace_stocks_dark.html' 
shutil.copy(archivo_origen, archivo_destino)

# Copy workspace_crypto in dark, but no it has style dark
archivo_origen = '/home/pi/bgeometrics.github.io/workspace_crypto.html'
archivo_destino = '/tmp/web/workspace_crypto_dark.html' 
shutil.copy(archivo_origen, archivo_destino)

# Copy dashboard_workspace_400 in dark, but no it has style dark
archivo_origen = '/home/pi/bgeometrics.github.io/dashboard_workspace_400.html'
archivo_destino = '/tmp/web/dashboard_workspace_400_dark.html' 
shutil.copy(archivo_origen, archivo_destino)

# Eliminate export data in m2*.html
remove_export_scripts_from_files([
    '/home/pi/bgeometrics.github.io/graphics/m2_global.html',
    '/home/pi/bgeometrics.github.io/graphics/m2_btc.html',
    '/home/pi/bgeometrics.github.io/graphics/m2_global_10w.html',
    '/home/pi/bgeometrics.github.io/graphics/m2_global_10w_300.html',
    '/home/pi/bgeometrics.github.io/graphics/m2_global_dark.html',
    '/home/pi/bgeometrics.github.io/graphics/m2_btc_dark.html',
    '/home/pi/bgeometrics.github.io/graphics/m2_global_10w_dark.html'
    '/home/pi/bgeometrics.github.io/graphics/m2_global_10w_300_dark.html'
])

print("")
print("For copy generate pages to project") 
print("cp /tmp/web/* /home/pi/bgeometrics.github.io/")
print("cd ..")
print("git commit -a -m... ")
print("git push")
print("")
