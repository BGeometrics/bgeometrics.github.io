function addUpgradePlotBand(chart, xAxisIndex, seriesData, opts) {
    opts = opts || {};
    var lastTimestamp = seriesData.length ? seriesData[seriesData.length - 1][0] : Date.now();
    var toTimestamp = Date.now();

    // Solo la zona sombreada; el texto se dibuja aparte (ver mas abajo) para que
    // no dependa del ancho en pixeles de la banda (puede ser minusculo si el
    // rango visible del grafico es de varios anos).
    chart.xAxis[xAxisIndex].addPlotBand({
        from: lastTimestamp,
        to: toTimestamp,
        color: opts.color || 'rgba(128,128,128,0.15)',
        zIndex: 5
    });

    var html = '<span style="display:inline-block;white-space:nowrap;background:' + (opts.badgeColor || '#F7931A') +
                ';color:' + (opts.textColor || '#000000') +
                ';padding:4px 10px;border-radius:12px;font-weight:bold;font-size:12px;' +
                'box-shadow:0 1px 3px rgba(0,0,0,0.4);">' +
                '<a href="' + (opts.loginUrl || 'https://portal.bgeometrics.com/login') +
                '" target="_blank" style="color:inherit;text-decoration:none;">' + (opts.loginLabel || 'Login') + '</a>' +
                ' / ' +
                '<a href="' + (opts.url || 'https://portal.bgeometrics.com/pricing') +
                '" target="_blank" style="color:inherit;text-decoration:none;">' + (opts.label || 'Upgrade') + '</a>' +
                '</span>';

    var badge = chart.renderer.label(html, 0, 0, undefined, undefined, undefined, true)
        .attr({ zIndex: 6 })
        .add();

    // Centra la etiqueta sobre la banda, pero sin dejar que se salga (ni se
    // recorte) del area del grafico cuando la banda es mas estrecha que el
    // propio texto.
    function reposition() {
        var axis = chart.xAxis[xAxisIndex];
        var xFrom = axis.toPixels(lastTimestamp);
        var xTo = axis.toPixels(toTimestamp);
        var bbox = badge.getBBox();
        var centerX = (xFrom + xTo) / 2;
        var minX = chart.plotLeft + bbox.width / 2 + 4;
        var maxX = chart.plotLeft + chart.plotWidth - bbox.width / 2 - 4;
        var x = Math.min(Math.max(centerX, minX), maxX);
        var y = chart.plotTop + chart.plotHeight / 2;
        badge.attr({ x: x - bbox.width / 2, y: y - bbox.height / 2 });
    }

    reposition();
    Highcharts.addEvent(chart, 'redraw', reposition);
}
