function addUpgradePlotBand(chart, xAxisIndex, seriesData, opts) {
    opts = opts || {};
    var lastTimestamp = seriesData.length ? seriesData[seriesData.length - 1][0] : Date.now();
    chart.xAxis[xAxisIndex].addPlotBand({
        from: lastTimestamp,
        to: Date.now(),
        color: opts.color || 'rgba(128,128,128,0.15)',
        zIndex: 5,
        label: {
            useHTML: true,
            align: 'center',
            verticalAlign: 'middle',
            rotation: 270,
            text: '<a href="' + (opts.url || 'https://portal.bgeometrics.com/pricing') +
                  '" target="_blank" style="display:inline-block;background:' + (opts.badgeColor || '#F7931A') +
                  ';color:' + (opts.textColor || '#000000') +
                  ';padding:4px 10px;border-radius:12px;font-weight:bold;font-size:12px;' +
                  'text-decoration:none;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,0.4);">' +
                  (opts.label || 'Upgrade') + '</a>'
        }
    });
}
