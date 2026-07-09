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
                  '" target="_blank" style="color:' + (opts.labelColor || '#888') +
                  ';font-weight:bold;text-decoration:none;">' + (opts.label || 'Upgrade') + '</a>'
        }
    });
}
