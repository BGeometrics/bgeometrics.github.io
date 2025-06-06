import os

directorio = '/tmp/web'  # Cambia si tus archivos están en otra carpeta

for nombre_archivo in os.listdir(directorio):
    if nombre_archivo.endswith('_dark.html'):
        ruta = os.path.join(directorio, nombre_archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()

        # Verifica si ya tiene una etiqueta canonical
        if '<link rel="canonical"' in contenido:
            print(f"{nombre_archivo} ya tiene una etiqueta canonical. Saltando.")
            continue

        # Extrae el nombre base sin _dark
        nombre_base = nombre_archivo.replace('_dark.html', '.html')
        url_canonical = f'<link rel="canonical" href="https://charts.bgeometrics.com/{nombre_base}">\n'

        # Inserta justo después de la etiqueta <head>
        if '<head>' in contenido:
            contenido = contenido.replace('<head>', f'<head>\n    {url_canonical}', 1)
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print(f"Canonical añadido a {nombre_archivo}")
        else:
            print(f"⚠ No se encontró <head> en {nombre_archivo}, no se añadió canonical.")

