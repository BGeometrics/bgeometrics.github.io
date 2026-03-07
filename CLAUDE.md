# BGeometrics — Contexto del proyecto

Sitio web estático de análisis on-chain de Bitcoin, publicado en GitHub Pages.
URL producción: `https://charts.bgeometrics.com`

## Generación de páginas

**Los archivos HTML del directorio raíz son generados automáticamente. No editarlos directamente.**

Para regenerar todas las páginas:

```bash
./tools/web-generation-pages-all.sh
```

Este script:
1. Activa el entorno virtual Python (`~/proyectos/bitcoin-scripts/bitcoin-scripts-env`)
2. Ejecuta los scripts Python de generación desde `tools/`
3. Genera variantes **light** y **dark** de cada página
4. Genera las páginas en **español** (`/es/` y `/es/graphics/`)
5. Establece los `canonical` de las páginas dark
6. Copia los resultados desde `/tmp/web/` al directorio raíz
7. Hace `git add`, `git commit` y `git push` automáticamente

El modo dark es el predeterminado: `index_dark.html` se copia sobre `index.html` al final.

## Estructura de plantillas (`tools/`)

| Fichero | Propósito |
|---|---|
| `web-generation-model.html` | Plantilla base (light) |
| `web-generation-model-dark.html` | Plantilla base (dark) |
| `web-generation-end-*.html` | Contenido HTML específico de cada página |
| `web-generation-pages-all.txt` | Lista de páginas: `file_name,file_end,title,iframe_html,description,keywords` |

Para añadir una nueva página:
1. Crear el archivo `web-generation-end-<nombre>.html` en `tools/`
2. Añadir la entrada en `web-generation-pages-all.txt`
3. Añadir la opción en el menú de `web-generation-model.html`
4. Ejecutar el script de generación

## Analytics

Google Analytics **eliminado**. No hay cookies de tracking. No se necesita banner de cookies.

## Estructura de directorios

```
/                   Páginas generadas (light y dark)
/es/                Versión en español
/es/graphics/       Gráficos traducidos al español
/tools/             Scripts de generación y plantillas
/assets/            CSS, JS, imágenes, vendors
/graphics/          Páginas de gráficos embebibles
/reports/           Informes
```

## Variantes de páginas

Cada página tiene dos variantes:
- `nombre.html` — tema claro
- `nombre_dark.html` — tema oscuro (es el predeterminado para el índice)

## Proyectos relacionados
BGapi es la API donde se exponen los endpoints
BGUser es el proyecto con el alta del usuario y las opciones de suscripción
BGsuggestion es el proyecto con las alertas 
bitcoin-scripts scripts de python donde se cargan algunos datos, se generan ficheros json y con diversas utilidades
bitcoin_metrics proyecto con la carga de datos bitcoin del full node a la base de datos PostgreSQL por bloque y diaria y con el cáculo de las métricas  
BGmcp es un proyecto MCP Server para conectarse a la API