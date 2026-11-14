#!/usr/bin/python3

"""
Genera graphics/hype_*.html desde hype-chart-template.html. Ejecutar desde tools/ al cambiar la
plantilla o la lista. Las variantes dark y es/ las saca web-generation-pages-all.sh.

Los datos los publica bitcoin-scripts/btc-file-hype-metrics.py: mantener la misma lista. Las
series internas de DefiLlama (hl_*) no tienen pagina: sus terminos prohiben republicarlas.

Al anadir una pagina: entrada en web-generation-pages-all.txt (grupo hyperliquid-nav), en el
menu Hyperliquid de las 14 plantillas web-generation-model*.html (tools/ y tools/es/) y en la
busqueda de assets/js/bgeometrics.js y es/assets/js/bgeometrics.js.
"""

ZERO_LINE = "\n                plotLines: [{ value: 0, width: 1, color: '#888888', zIndex: 3 }],"
LOG_AXIS = "\n                type: 'logarithmic',"
COLUMNS = "\n                type: 'column',"
# Media de la tasa horaria -> % anualizado (24 x 365 horas)
ANNUALIZED = ".map(([ts, val]) => [ts, val == null ? null : val * 24 * 365 * 100])"

# pagina, nombre, decimales y opciones ('selected': boton de zoom inicial, 4 = 1y, por defecto 6 = All)
CHARTS = [
    ('hype_market_cap', 'Market Cap', 0, {'axis': LOG_AXIS, 'suffix': ' USD'}),
    ('hype_mcap_fdv_ratio', 'Market Cap / FDV', 2, {'suffix': ' %'}),
    ('hype_funding_rate', 'Funding Rate (annualized)', 2, {'axis': ZERO_LINE, 'suffix': ' %', 'transform': ANNUALIZED}),
]


def tooltip_suffix(suffix):
    if not suffix:
        return ''
    return ",\n                    valueSuffix: '" + suffix + "'"


def main():
    with open('hype-chart-template.html', encoding='utf-8') as file:
        template = file.read()

    for metric, name, decimals, options in CHARTS:
        page = template
        page = page.replace('__TITLE__', 'Hyperliquid ' + name)
        page = page.replace('__SLUG__', metric.replace('_', '-'))
        page = page.replace('__METRIC__', metric)
        page = page.replace('__NAME__', name)
        page = page.replace('__DECIMALS__', str(decimals))
        page = page.replace('__TRANSFORM__', options.get('transform', ''))
        page = page.replace('__AXIS_OPTIONS__', options.get('axis', ''))
        page = page.replace('__SERIES_OPTIONS__', options.get('series', ''))
        page = page.replace('__SUFFIX__', tooltip_suffix(options.get('suffix')))
        page = page.replace('__SELECTED__', str(options.get('selected', 6)))

        with open('../graphics/' + metric + '.html', 'w', encoding='utf-8', newline='\n') as file:
            file.write(page.replace('\r\n', '\n'))


if __name__ == '__main__':
    main()
