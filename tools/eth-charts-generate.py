#!/usr/bin/python3

"""
Genera graphics/eth_*.html desde eth-chart-template.html. Ejecutar desde tools/ al cambiar la
plantilla o la lista. Las variantes dark y es/ las saca web-generation-pages-all.sh.

Los datos los publica bitcoin-scripts/btc-file-eth-metrics.py: mantener la misma lista.
"""

ZERO_LINE = "\n                plotLines: [{ value: 0, width: 1, color: '#888888', zIndex: 3 }],"
ONE_LINE = "\n                plotLines: [{ value: 1, width: 1, color: '#888888', zIndex: 3 }],"
LOG_AXIS = "\n                type: 'logarithmic',"
COLUMNS = "\n                type: 'column',"
PERCENT = ".map(([ts, val]) => [ts, val == null ? null : val * 100])"

# pagina, nombre, decimales y opciones
CHARTS = [
    ('eth_sopr', 'SOPR', 3, {'axis': ONE_LINE}),
    ('eth_mvrv', 'MVRV', 3, {'axis': ONE_LINE}),
    ('eth_mvrv_zscore', 'MVRV Z-Score', 2, {'axis': ZERO_LINE}),
    ('eth_nupl', 'NUPL', 3, {'axis': ZERO_LINE}),
    ('eth_realized_price', 'Realized Price', 2, {'axis': LOG_AXIS, 'suffix': ' USD'}),
    ('eth_realized_cap', 'Realized Cap', 0, {'axis': LOG_AXIS, 'suffix': ' USD'}),
    ('eth_net_realized_pl', 'Net Realized Profit/Loss', 0, {'axis': ZERO_LINE, 'series': COLUMNS, 'suffix': ' USD'}),
    ('eth_supply', 'Supply', 0, {'suffix': ' ETH'}),
    ('eth_market_cap', 'Market Cap', 0, {'axis': LOG_AXIS, 'suffix': ' USD'}),
    ('eth_staked', 'Staked', 0, {'suffix': ' ETH'}),
    ('eth_staking_deposits', 'Staking Deposits', 0, {'series': COLUMNS, 'suffix': ' ETH'}),
    ('eth_staking_realized_price', 'Staking Realized Price', 2, {'axis': LOG_AXIS, 'suffix': ' USD'}),
    ('eth_staking_mvrv', 'Staking MVRV', 3, {'axis': ONE_LINE}),
    ('eth_active_addresses', 'Active Addresses', 0, {}),
    ('eth_new_addresses', 'New Addresses', 0, {}),
    ('eth_addresses', 'Total Addresses', 0, {}),
    ('eth_txs', 'Transactions', 0, {}),
    ('eth_total_volume', 'Total Volume', 0, {'suffix': ' ETH'}),
    ('eth_active_1y', 'Supply Last Active 1y+', 2, {'suffix': ' %', 'transform': PERCENT}),
    ('eth_total_tx_fees', 'Total Fees', 2, {'suffix': ' ETH'}),
    ('eth_total_tx_fees_usd', 'Total Fees USD', 0, {'suffix': ' USD'}),
    ('eth_total_gas_used', 'Total Gas Used', 0, {}),
    ('eth_mean_tx_gas_price', 'Mean Gas Price', 0, {'suffix': ' wei'}),
    ('eth_etf_flows_usd', 'ETF Flows USD', 0, {'axis': ZERO_LINE, 'series': COLUMNS, 'suffix': ' USD'}),
]


def tooltip_suffix(suffix):
    if not suffix:
        return ''
    return ",\n                    valueSuffix: '" + suffix + "'"


def main():
    with open('eth-chart-template.html', encoding='utf-8') as file:
        template = file.read()

    for metric, name, decimals, options in CHARTS:
        page = template
        page = page.replace('__TITLE__', 'Ethereum ' + name)
        page = page.replace('__SLUG__', metric.replace('_', '-'))
        page = page.replace('__METRIC__', metric)
        page = page.replace('__NAME__', name)
        page = page.replace('__DECIMALS__', str(decimals))
        page = page.replace('__TRANSFORM__', options.get('transform', ''))
        page = page.replace('__AXIS_OPTIONS__', options.get('axis', ''))
        page = page.replace('__SERIES_OPTIONS__', options.get('series', ''))
        page = page.replace('__SUFFIX__', tooltip_suffix(options.get('suffix')))

        with open('../graphics/' + metric + '.html', 'w', encoding='utf-8', newline='\n') as file:
            file.write(page)


if __name__ == '__main__':
    main()
