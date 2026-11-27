#!/usr/bin/python3

"""
Genera graphics/exchange_*.html (menu "Exchange flows") y graphics/miner_*_flow*.html
(menu "Miners", MINER_CHARTS) desde exchange-chart-template.html.
Ejecutar desde tools/ al cambiar la plantilla o la lista. Las variantes dark y es/ las saca
web-generation-pages-all.sh.

Los JSON los publica bitcoin-scripts/btc-file-exchange-flows-venus.py (gating estandar:
4 anos y embargo de 7 dias). Los suscriptores leen /chart/<slug> (endpoints /v1/exchange-*).

Al anadir una pagina: entrada en web-generation-pages-all.txt (grupo exchange-nav), su
web-generation-end-<pagina>.html (tools/ y tools/es/), el menu "Exchange flows" de las 14
plantillas web-generation-model*.html (tools/ y tools/es/) y la busqueda de
assets/js/bgeometrics.js y es/assets/js/bgeometrics.js.

Mineros: igual, pero grupo miners-nav y menu "Miners"; los JSON los publica
bitcoin-scripts/btc-file-miner-flows-venus.py (endpoints /v1/miner-*).
"""

ZERO_LINE = "\n                plotLines: [{ value: 0, width: 1, color: '#888888', zIndex: 3 }],"
PERCENT = ".map(([ts, val]) => [ts, val == null ? null : val * 100])"

RED = '#e74c3c'
GREEN = '#2ecc71'
ORANGE = '#f7931a'
BLUE = '#3498db'

# Zonas por signo: positivo (entra BTC a exchanges, presion vendedora) rojo; negativo verde.
SIGN_ZONES = "\n                zoneAxis: 'y',\n                zones: [{ value: 0, color: '" + GREEN + "' }, { color: '" + RED + "' }],"
# Mineros al reves: positivo (acumulan) verde; negativo (gastan reservas, presion vendedora) rojo.
SIGN_ZONES_INVERSE = "\n                zoneAxis: 'y',\n                zones: [{ value: 0, color: '" + RED + "' }, { color: '" + GREEN + "' }],"


def s(var, slug, file, name, color, decimals, field=None, suffix='', kind=None,
      transform='', zones=False, visible=True, ma_of=None, ma=None, grouping=None):
    return dict(var=var, slug=slug, file=file, name=name, color=color, decimals=decimals,
                field=field, suffix=suffix, kind=kind, transform=transform, zones=zones,
                visible=visible, ma_of=ma_of, ma=ma, grouping=grouping)


# pagina, titulo, nombre del eje, series, opciones ('selected': zoom inicial, 4 = 1y, 6 = All)
CHARTS = [
    ('exchange_netflow', 'Exchange Netflow (BTC)', 'Netflow (BTC)', [
        s('data_netflow', 'exchange-netflow-btc', 'exchange_netflow_btc', 'Exchange Netflow', RED, 2,
          suffix=' BTC', kind='column', zones=True),
        s('data_netflow_7dma', None, None, 'Netflow 7D MA', ORANGE, 2, suffix=' BTC',
          ma_of='data_netflow', ma=7, visible=False),
        s('data_netflow_30dma', None, None, 'Netflow 30D MA', BLUE, 2, suffix=' BTC',
          ma_of='data_netflow', ma=30, visible=False),
    ], {'axis': ZERO_LINE, 'selected': 4}),
    ('exchange_inflow_outflow', 'Exchange Inflow and Outflow (BTC)', 'BTC', [
        s('data_inflow', 'exchange-inflow-btc', 'exchange_inflow_btc', 'Exchange Inflow', RED, 2, suffix=' BTC'),
        s('data_outflow', 'exchange-outflow-btc', 'exchange_outflow_btc', 'Exchange Outflow', GREEN, 2, suffix=' BTC'),
    ], {'selected': 4}),
    ('exchange_inflow_outflow_usd', 'Exchange Inflow and Outflow (USD)', 'USD', [
        s('data_inflow', 'exchange-inflow-usd', 'exchange_inflow_usd', 'Exchange Inflow', RED, 0, suffix=' USD'),
        s('data_outflow', 'exchange-outflow-usd', 'exchange_outflow_usd', 'Exchange Outflow', GREEN, 0, suffix=' USD'),
    ], {'selected': 4}),
    ('exchange_reserve', 'Exchange Reserve (BTC)', 'Reserve (BTC)', [
        s('data_reserve', 'exchange-reserve-btc', 'exchange_reserve_btc', 'Exchange Reserve', ORANGE, 0, suffix=' BTC'),
    ], {}),
    ('exchange_reserve_usd', 'Exchange Reserve (USD)', 'Reserve (USD)', [
        s('data_reserve', 'exchange-reserve-usd', 'exchange_reserve_usd', 'Exchange Reserve', ORANGE, 0, suffix=' USD'),
    ], {}),
    ('exchange_supply_ratio', 'Exchange Supply Ratio', 'Supply on exchanges (%)', [
        s('data_ratio', 'exchange-supply-ratio', 'exchange_supply_ratio', 'Exchange Supply Ratio', ORANGE, 2,
          suffix=' %', transform=PERCENT),
    ], {}),
    ('exchange_reserve_change', 'Exchange Reserve 30-Day Change', '30D change (BTC)', [
        s('data_change', 'exchange-reserve-trend', 'exchange_reserve_change_30d_btc', 'Reserve 30D Change', RED, 0,
          field='reserveChange30dBtc', suffix=' BTC', kind='column', zones=True, grouping='average'),
    ], {'axis': ZERO_LINE}),
    ('exchange_tx_count', 'Exchange Inflow and Outflow Transactions', 'Transactions', [
        s('data_inflow', 'exchange-inflow-tx-count', 'exchange_inflow_tx_count', 'Inflow Transactions', RED, 0),
        s('data_outflow', 'exchange-outflow-tx-count', 'exchange_outflow_tx_count', 'Outflow Transactions', GREEN, 0),
    ], {'selected': 4}),
    ('exchange_mean_size', 'Exchange Mean Inflow and Outflow Size', 'BTC per transaction', [
        s('data_inflow', 'exchange-inflow-mean-btc', 'exchange_inflow_mean_btc', 'Mean Inflow', RED, 2, suffix=' BTC'),
        s('data_outflow', 'exchange-outflow-mean-btc', 'exchange_outflow_mean_btc', 'Mean Outflow', GREEN, 2, suffix=' BTC'),
    ], {'selected': 4}),
    ('exchange_to_exchange', 'Exchange to Exchange Flow', 'BTC', [
        s('data_e2e', 'exchange-to-exchange-flow', 'exchange_to_exchange_btc', 'Exchange to Exchange Flow', BLUE, 2,
          suffix=' BTC'),
    ], {'selected': 4}),
]

# Flujos de mineros (miner_day en Venus). Outflow = BTC que salen de las direcciones de mineros
# (posible venta), en rojo; inflow (coinbase + recibidos) en verde.
MINER_CHARTS = [
    ('miner_netflow', 'Miner Netflow (BTC)', 'Netflow (BTC)', [
        s('data_netflow', 'miner-net-flow', 'miner_netflow_btc', 'Miner Netflow', GREEN, 2,
          suffix=' BTC', kind='column', zones='inverse'),
        s('data_netflow_7dma', None, None, 'Netflow 7D MA', ORANGE, 2, suffix=' BTC',
          ma_of='data_netflow', ma=7, visible=False),
        s('data_netflow_30dma', None, None, 'Netflow 30D MA', BLUE, 2, suffix=' BTC',
          ma_of='data_netflow', ma=30, visible=False),
    ], {'axis': ZERO_LINE, 'selected': 4}),
    ('miner_inflow_outflow', 'Miner Inflow and Outflow (BTC)', 'BTC', [
        s('data_inflow', 'miner-inflow', 'miner_inflow_btc', 'Miner Inflow', GREEN, 2, suffix=' BTC'),
        s('data_outflow', 'miner-outflow', 'miner_outflow_btc', 'Miner Outflow', RED, 2, suffix=' BTC'),
    ], {'selected': 4}),
    ('miner_inflow_outflow_usd', 'Miner Inflow and Outflow (USD)', 'USD', [
        s('data_inflow', 'miner-inflow-usd', 'miner_inflow_usd', 'Miner Inflow', GREEN, 0, suffix=' USD'),
        s('data_outflow', 'miner-outflow-usd', 'miner_outflow_usd', 'Miner Outflow', RED, 0, suffix=' USD'),
    ], {'selected': 4}),
    ('miner_reserve_btc', 'Miner Reserve (BTC)', 'Reserve (BTC)', [
        s('data_reserve', 'miner-reserve', 'miner_reserve_btc', 'Miner Reserve', ORANGE, 0, suffix=' BTC'),
    ], {}),
    ('miner_reserve_usd', 'Miner Reserve (USD)', 'Reserve (USD)', [
        s('data_reserve', 'miner-reserve-usd', 'miner_reserve_usd', 'Miner Reserve', ORANGE, 0, suffix=' USD'),
    ], {}),
    ('miner_reserve_change', 'Miner Reserve 30-Day Change (%)', '30D change (%)', [
        s('data_change', 'miner-reserve-change-30d-pct', 'miner_reserve_change_30d_pct', 'Reserve 30D Change',
          GREEN, 3, suffix=' %', kind='column', zones='inverse', grouping='average'),
    ], {'axis': ZERO_LINE}),
]

# grupo -> fichero de precio (lo escribe el script de JSON de cada grupo)
GROUPS = [
    (CHARTS, 'exchange_flows_btc_price'),
    (MINER_CHARTS, 'miner_flows_btc_price'),
]


def load_line(serie):
    if serie['ma_of']:
        return "            const %s = bgRollingMean(%s, %d);" % (serie['var'], serie['ma_of'], serie['ma'])
    field = ", '" + serie['field'] + "'" if serie['field'] else ''
    return ("            const %s = (await bgSeries('%s', 'https://charts.bgeometrics.com/files/%s.json'%s))%s;"
            % (serie['var'], serie['slug'], serie['file'], field, serie['transform']))


def series_block(serie):
    lines = ["            }, {",
             "                id: '%s'," % serie['name'],
             "                name: '%s'," % serie['name']]
    if serie['kind']:
        lines.append("                type: '%s'," % serie['kind'])
    lines.append("                color: '%s'," % serie['color'])
    if serie['zones']:
        lines.append((SIGN_ZONES_INVERSE if serie['zones'] == 'inverse' else SIGN_ZONES).strip('\n'))
    if serie['grouping']:
        # Las columnas se agrupan por defecto sumando: correcto para flujos (netflow semanal),
        # no para niveles como la variacion a 30 dias, que debe promediarse.
        lines.append("                dataGrouping: { approximation: '%s' }," % serie['grouping'])
    if not serie['visible']:
        lines.append("                visible: false,")
    lines.append("                data: %s," % serie['var'])
    tooltip = "                    valueDecimals: %d" % serie['decimals']
    if serie['suffix']:
        tooltip += ",\n                    valueSuffix: '%s'" % serie['suffix']
    lines += ["                tooltip: {", tooltip, "                },", "                yAxis: 0"]
    return "\n".join(lines)


def main():
    with open('exchange-chart-template.html', encoding='utf-8') as file:
        template = file.read()

    pages = [(chart, price) for charts, price in GROUPS for chart in charts]
    for (page_name, name, axis_name, series, options), price in pages:
        page = template.replace('/files/exchange_flows_btc_price.json', '/files/' + price + '.json')
        page = page.replace('__TITLE__', 'Bitcoin ' + name)
        page = page.replace('__NAME__', name)
        page = page.replace('__AXIS_NAME__', axis_name)
        page = page.replace('__AXIS_OPTIONS__', options.get('axis', ''))
        page = page.replace('__LOAD__', "\n".join(load_line(x) for x in series))
        page = page.replace('__SERIES__', "\n".join(series_block(x) for x in series))
        page = page.replace('__BAND_DATA__', series[0]['var'])
        page = page.replace('__SELECTED__', str(options.get('selected', 6)))

        with open('../graphics/' + page_name + '.html', 'w', encoding='utf-8', newline='\n') as file:
            file.write(page)


if __name__ == '__main__':
    main()
