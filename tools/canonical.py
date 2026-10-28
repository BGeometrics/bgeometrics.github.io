import os
import re

directorio = '/tmp/web'  # Cambia si tus archivos están en otra carpeta
base_url = 'https://charts.bgeometrics.com/'

# Recorre el raíz y los subdirectorios (es/) generados en /tmp/web
for raiz, _, archivos in os.walk(directorio):
    for nombre_archivo in archivos:
        if not nombre_archivo.endswith('.html'):
            continue

        ruta = os.path.join(raiz, nombre_archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()

        # Verifica si ya tiene una etiqueta canonical
        if '<link rel="canonical"' in contenido:
            print(f"{ruta} ya tiene una etiqueta canonical. Saltando.")
            continue

        # Páginas dark -> versión light; resto -> la propia página (sin parámetros)
        nombre_base = nombre_archivo.replace('_dark.html', '.html')
        ruta_relativa = os.path.relpath(os.path.join(raiz, nombre_base), directorio).replace(os.sep, '/')
        url_canonical = f'<link rel="canonical" href="{base_url}{ruta_relativa}">\n'

        # Inserta justo después de la etiqueta <head>
        nuevo, n = re.subn(r'<head(\s[^>]*)?>', lambda m: f'{m.group(0)}\n  {url_canonical}', contenido, count=1)
        if n:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(nuevo)
            print(f"Canonical añadido a {ruta}")
        else:
            print(f"⚠ No se encontró <head> en {ruta}, no se añadió canonical.")
