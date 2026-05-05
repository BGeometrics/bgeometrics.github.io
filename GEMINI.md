# BGeometrics Web - Guía de Front-end

Este repositorio contiene el sitio web estático de análisis on-chain de Bitcoin, publicado en GitHub Pages.

## Mandatos Críticos
- **No editar HTML en el raíz**: Los archivos HTML del directorio raíz son autogenerados. Cualquier cambio manual se perderá.
- **Privacidad**: No se utiliza Google Analytics ni cookies de tracking. No añadir scripts que requieran banners de cookies.

## Flujo de Generación
Para regenerar el sitio completo (menús, variantes dark/light, traducciones):

```bash
./tools/web-generation-pages-all.sh
```

### Proceso de Automatización
1. Utiliza el entorno virtual Python de `bitcoin-scripts`.
2. Procesa las plantillas en `tools/` para generar las variantes.
3. El tema **oscuro** (`index_dark.html`) es el predeterminado y se copia como `index.html`.
4. Los resultados se despliegan automáticamente tras la generación.

## Estructura de Plantillas (`tools/`)
- `web-generation-model.html`: Base para el tema claro.
- `web-generation-model-dark.html`: Base para el tema oscuro.
- `web-generation-end-<nombre>.html`: Fragmento de contenido específico para cada página.
- `web-generation-pages-all.txt`: Configuración de páginas (nombres, títulos, descriptions).

### Cómo añadir una nueva página
1. Crear el fragmento HTML en `tools/web-generation-end-<nombre>.html`.
2. Registrar la página en `tools/web-generation-pages-all.txt`.
3. Actualizar la navegación en los archivos `model.html` correspondientes.
4. Ejecutar el script de generación.

## Organización de Directorios
- `/`: Raíz con páginas generadas.
- `/es/`: Versión en español (incluyendo `/graphics/`).
- `/tools/`: Scripts de orquestación y plantillas base.
- `/assets/`: Recursos estáticos (CSS, JS, imágenes).
- `/graphics/`: Páginas HTML dedicadas exclusivamente a embeber gráficos.
- `/reports/`: Informes generados periódicamente.

## Estándares de Navegación
El orden de la cabecera debe ser consistente en todas las páginas:
`Charts` → `Reports` → `API` → `Pricing` | `Workspace` | `Login` | `X` | `[theme toggle]`
