/**
 */
var names = [
{ name: "Bitcoin Price USD", link: "reports/bitcoin_price_usd_g.html" },
{ name: "Bitcoin Capitalization", link: "capitalization.html" },
{ name: "Bitcoin Realized Capitalization", link: "capitalization.html" },
{ name: "Bitcoin Investor Capitalization", link: "capitalization.html" },
{ name: "Bitcoin Thermo Capitalization", link: "capitalization.html" },
{ name: "SOPR (Spent Output Profit Ratio)", link: "sopr.html" },
{ name: "LTH-SOPR (Long Term Hodler)", link: "sopr.html" },
{ name: "STH-SOPR (Short Term Hodler)", link: "sopr.html" },
{ name: "Bitcoin MVRV (Market Value Realized Value)", link: "mvrv.html" },
{ name: "Bitcoin MVRV Z-Score", link: "mvrv.html" },
{ name: "MVRV, LTH (Long Term Hodler) and STH (Short Term Hodler)", link: "mvrv.html" },
{ name: "Bitcoin Coin Days Destroyed (CDD)", link: "cdd.html" },
{ name: "CDD Terminal Adjusted 90-Day", link: "cdd.html" },
{ name: "Bitcoin, SP500 or S&P 500, Gold, Tesla", link: "graphics/sp500_gold.html" },
{ name: "Bitcoin Coin and Address Distribution Table", link: "reports/bitcoin_distribution_tables.html" },
{ name: "Bitcoin Coin Distribution", link: "graphics/distribution_coin.html" },
{ name: "Bitcoin Address Distribution", link: "graphics/distribution_addr.html" },
{ name: "Bitcoin OHLC (Open High Low Close)", link: "ohlc.html" },
{ name: "NUPL (Net Unrealized Profit / Loss)", link: "reports/bitcoin_nupl_g.html" },
{ name: "Hodl Waves Realized Cap", link: "reports/bitcoin_reacap_hodl_waves_g.html" },
{ name: "Short Term Hodler (STH) Realized Price", link: "reports/bitcoin_realized_short_g.html" },
{ name: "Hodl Waves", link: "hodl_waves.html" },
{ name: "Change BTC on exchanges", link: "reports/bitcoin_ex_change_held_g.html" },
{ name: "Bitcoin Fear and Greed", link: "reports/bitcoin_fear_greed_g.html" },
{ name: "AVIV (Asset Value to Investor Value) Ratio", link: "reports/bitcoin_aviv_g.html" },
{ name: "Bitcoin Halving Cycle", link: "reports/bitcoin_halving_cycle_g.html" },
{ name: "BTC price history and halving timeline", link: "reports/bitcoin_price_g_log.html" },
{ name: "Bitcoin Halving Radar", link: "reports/bitcoin_halving_radar_g.html" },
{ name: "Bitcoin Years Candles", link: "reports/bitcoin_year_candle_g.html" },
{ name: "Influence of the halving on the monthly price of bitcoin", link: "reports/bitcoin_halving_month_g.html" },
{ name: "Bitcoin Distribution Coin", link: "reports/bitcoin_distribution_coin_g.html" },
{ name: "Whale Accumulation Heat Map", link: "reports/bitcoin_whale_accumulation_heatmap_g.html" },
{ name: "Bitcoin distribution Humpback >10K", link: "reports/bitcoin_distribution_coin_g_humpback.html" },
{ name: "Bitcoin distribution Whale 1000-10K", link: "reports/bitcoin_distribution_coin_g_whale.html" },
{ name: "Whale (1K-10K) Net Position BTC in 30d", link: "reports/bitcoin_whale_30d_sum_g.html" },
{ name: "Shark (100-1000) Net Position BTC 30d", link: "reports/bitcoin_shark_30d_sum_g.html" },
{ name: "Bitcoin realized price distribution (URPD)", link: "graphics/distribution_realized_price.html" },
{ name: "History bitcoin price on a day like today", link: "reports/bitcoin_price_usd_day_g.html" },
{ name: "Bitcoin Volatility", link: "reports/bitcoin_volatility_g.html" },
{ name: "Bitcoin Dominance", link: "reports/bitcoin_dominance_g.html" },
{ name: "Bitcoin Daily Price Performance", link: "reports/bitcoin_daily_price_performance_g.html" },
{ name: "Bitcoin Liveniness", link: "reports/bitcoin_liveliness_g.html" },
{ name: "Bitcoin S&P 500 correlation (Plotly)", link: "reports/bitcoin_sp500_correlation_g.html" },
{ name: "MVRV Z-Score (Plotly)", link: "reports/bitcoin_mvrv_zscore_g.html" },
{ name: "Bitcoin Realized Price (Plotly)", link: "reports/bitcoin_realized_price_g.html" },
{ name: "Day moving average (Plotly)", link: "reports/bitcoin_200_moving_average_g.html" },
{ name: "Bitcoin Coin Destroyed Days Terminal Adjusted 90d (Plotly)", link: "reports/bitcoin_cdd_ajusted_90dma_g.html" },
{ name: "Long Term Hodler vs Short Term Hodler", link: "reports/bitcoin_lth_sth_g.html" },
{ name: "Services, custom charts, graphics", link: "services.html" },
{ name: "Open Interest Futures", link: "open_interest_futures.html" },
{ name: "ETF Total Balance", link: "etf.html" },
{ name: "ETF BTC Held", link: "etf_btc.html" },
{ name: "Price Live", link: "ohlc_1m.html" },
{ name: "OHLC Week", link: "ohlc_7d.html" },
{ name: "Pi Cycle", link: "pi_cycle.html" },
{ name: "Addresses Active", link: "address_active.html" },
{ name: "Stablecoin Supply", link: "stablecoin_supply.html" },
{ name: "BTC Power Law", link: "power_law.html" },
{ name: "S&P 500 Gold Tesla MSTR", link: "sp500_gold.html" },
{ name: "M2 Money Stock", link: "m2.html" },
{ name: "Fed Funds", link: "fedfunds.html" },
{ name: "Donation", link: "donation.html" },
{ name: "BGeometrics Workspace", link: "workspace.html" },
];

function search() {
var searchQuery = document.getElementById('searchInput').value.toLowerCase();
var results = [];

for (var i = 0; i < names.length; i++) {
    if (names[i].name.toLowerCase().includes(searchQuery)) {
    results.push(names[i]);
    }
}

displayResults(results);
}

function displayResults(results) {
    var resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No results found.</p>';
    } else {
        resultsContainer.innerHTML = '<ul>';

        for (var j = 0; j < results.length; j++) {
        resultsContainer.innerHTML += '<li><a href="' + results[j].link + '" target="_blank">' + results[j].name + '</a></li>';
        }

        resultsContainer.innerHTML += '</ul></br>';
    }
}

function handleKeyPress(event) {
    if (event.keyCode === 13) {
        search(); 
        event.preventDefault();
    }
}

function addCharts(_metricId, _text){
    var e = document.getElementById("metrics");
    var text;
    var yAxis = 0;

    if (_metricId.indexOf('_axis') > 0) {
        _metricId = _metricId.substring(0, _metricId.indexOf('_axis'));
        yAxis = 1;
    }
    else if (_metricId.indexOf('_2axis') > 0) {
        _metricId = _metricId.substring(0, _metricId.indexOf('_2axis'));
        yAxis = 2;
    }
    else if (_metricId.indexOf('_3axis') > 0) {
        _metricId = _metricId.substring(0, _metricId.indexOf('_3axis'));
        yAxis = 3;
    }
    else if (_metricId.indexOf('_4axis') > 0) {
        _metricId = _metricId.substring(0, _metricId.indexOf('_4axis'));
        yAxis = 4;
    }
    data = fetch('https://charts.bgeometrics.com/files/' + _metricId + '.json')
        .then(response => response.json());

    Promise.all([data]).then(values => {
        chart.addSeries({
            id: _metricId,
            name: _text,
            data: values[0],
            tooltip: {
                valueDecimals: 2
            },
            yAxis: yAxis
            
        });
    });
}

function setCookie(_metricsId){
    var cookieString = COOKIE_NAME + "=" + _metricsId;
    var date = new Date();
    date.setTime(date.getTime() + (90*24*60*60*1000)); // cookie 90 days
    expires = "; expires=" + date.toUTCString();
    document.cookie = cookieString + expires + "; path=/";
    //console.log("Set cookie " + cookieString + expires);

    return _metricsId
}

function getCookieValue(name) {
    const regex = new RegExp(`(^| )${name}=([^;]+)`)
    const match = document.cookie.match(regex)
    if (match) {
        return match[2]
    }
}

function deleteCookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    //console.log("Delete cookie " + name);
}

function changeMetrics() {
    var e = document.getElementById("metrics");
    var value = e.value;
    var text = e.options[e.selectedIndex].text;

    // Show halvings
    if(value == "halving") {

        chart.xAxis[0].update({
              plotLines: [{
                    name: '1st halving',
                    label: {
                        text:'1st halving',
                    },
                    color: '#777777',
                    dashStyle: 'Dash',
                    value: 1354060800000
              }, {
                    name: '2nd halving',
                    label: {
                        text:'2nd halving',
                    },
                    color: '#777777',
                    dashStyle: 'Dash',
                    value: 1468022400000
              }, {
                    name: '3rd halving',
                    label: {
                        text:'3rd halving',
                    },
                    color: '#777777',
                    dashStyle: 'Dash',
                    value: 1589155200000
              }, {
                    name: '4th halving',
                    label: {
                        text:'4th halving',
                    },
                    color: '#777777',
                    dashStyle: 'Dash',
                    value: 1713571200000
              }
            ]
        });
    }
    else if(value == "relevant") {
        chart.xAxis[0].update({
              plotLines: [{
                    name: '1st halving',
                    label: {
                        text:'1st halving',
                    },
                    color: '#777777',
                    dashStyle: 'Dash',
                    value: 1354060800000
              }, {
                    name: '2nd halving',
                    label: {
                        text:'2nd halving',
                    },
                    color: '#777777',
                    dashStyle: 'Dash',
                    value: 1468022400000
              }, {
                    name: '3rd halving',
                    label: {
                        text:'3rd halving',
                    },
                    color: '#777777',
                    dashStyle: 'Dash',
                    value: 1589155200000
              }, {
                    name: '4th halving',
                    label: {
                        text:'4th halving',
                    },
                    color: '#777777',
                    dashStyle: 'Dash',
                    value: 1713571200000
              }, {
                    name: 'COVID-19',
                    label: {
                        text:'COVID-19',
                    },
                    color: 'red',
                    dashStyle: 'Dash',
                    value: 1584662400000
              }, {
                    name: 'Russia Ukraine War',
                    label: {
                        text:'Russia Ukraine War',
                    },
                    color: 'red',
                    dashStyle: 'Dash',
                    value: 1645660800000
              }, {
                    name: 'ETFs debut',
                    label: {
			text:'ETFs debut',
                    },
                    color: 'green',
                    dashStyle: 'Dash',
                    value: 1704931200000
              }, {
                    name: 'Fork BCH',
                    label: {
			text:'Fork BCH',
                    },
                    color: 'green',
                    dashStyle: 'Dash',
                    value: 1501545600000
              }, {
                    name: 'Mt. Gox close',
                    label: {
			text:'Mt. Gox close',
                    },
                    color: 'red',
                    dashStyle: 'Dash',
                    value: 1393545600000
              }, {
                    name: 'FBI closes Silk Road',
                    label: {
			text:'FBI closes Silk Road',
                    },
                    color: 'green',
                    dashStyle: 'Dash',
                    value: 1380672000000
              }
            ]
        });
    }
    else if(value == "bull_bear") {
        // 2010-10-04 2011-06-06 
        chart.xAxis[0].addPlotBand({
            from: 1286150400000,
            to: 1307318400000,
            color: 'rgb(144, 237, 125, 0.2)',
        });
        // 2011-06-06 2011-11-18  
        chart.xAxis[0].addPlotBand({
            from: 1307318400000,
            to: 1321574400000,
            color: 'rgba(255, 0, 0, 0.15)',
        });
        // 2011-11-18 2013-04-09 
        chart.xAxis[0].addPlotBand({
            from: 1321574400000,
            to: 1365465600000,
            color: 'rgb(144, 237, 125, 0.2)',
        });
        // 2013-04-09 2013-07-06 
        chart.xAxis[0].addPlotBand({
            from: 1365465600000,
            to: 1373068800000,
            color: 'rgba(255, 0, 0, 0.15)',
        });
        // 2013-07-06 2013-11-29 
        chart.xAxis[0].addPlotBand({
            from: 1373068800000,
            to: 1385683200000,
            color: 'rgb(144, 237, 125, 0.2)',
        });
        // 2013-11-29 2015-01-14 
        chart.xAxis[0].addPlotBand({
            from: 1385683200000,
            to: 1420329600000,
            color: 'rgba(255, 0, 0, 0.15)',
        });
        // 2015-01-14 2017-12-17 
        chart.xAxis[0].addPlotBand({
            from: 1420329600000,
            to: 1513468800000, 
            color: 'rgb(144, 237, 125, 0.2)',
                //zIndex: 3
        });
        //2017-12-17 2018-12-15
        chart.xAxis[0].addPlotBand({
            from: 1513468800000, 
            to: 1544832000000, 
            color: 'rgba(255, 0, 0, 0.15)',
        });
        //2018-12-15 2021-04-12
        chart.xAxis[0].addPlotBand({
            from: 1544832000000,
            to: 1618185600000,  
            color: 'rgb(144, 237, 125, 0.2)',
        });

        //2021-04-12 2021-07-20
        chart.xAxis[0].addPlotBand({
            from: 1618185600000,
            to: 1626739200000,  
            color: 'rgba(255, 0, 0, 0.15)',
        });

        //2021-07-20 2021-11-08
        chart.xAxis[0].addPlotBand({
            from: 1626739200000,  
            to: 1636329600000,  
            color: 'rgb(144, 237, 125, 0.2)',
        });

        //2021-11-08 2022-12-26
        chart.xAxis[0].addPlotBand({
            from: 1636329600000,  
            to: 1672012800000,  
            color: 'rgba(255, 0, 0, 0.15)',
        });

        //2022-12-26 ...
        chart.xAxis[0].addPlotBand({
            from: 1672012800000,
            to: 1767225600000,  
            color: 'rgb(144, 237, 125, 0.2)',
        });
    }
    else if(value == "max_pain") {
        // 2015-01-03 2015-10-12 
        chart.xAxis[0].addPlotBand({
            from: 1420243200000,
            to: 1444608000000,
            color: 'rgb(0, 0, 255, 0.3)',
        });
        // 2018-11-22 2019-03-28  
        chart.xAxis[0].addPlotBand({
            from: 1542844800000,
            to: 1553731200000,
            color: 'rgb(0, 0, 255, 0.3)',
        });
        // 2022-08-22 2023-01-09  
        chart.xAxis[0].addPlotBand({
            from: 1661126400000,
            to: 1673222400000,
            color: 'rgb(0, 0, 255, 0.3)',
        });
    }
    else if(value == "zone_0") {
        chart.addSeries({
            data: data,
            zones: [{
                value: 0,
                color: 'blue'
            }]
        
        });
    }
    else {
        // set cookie
        if(!metricsId.includes(value)){
            if(metricsId.length == 0) 
                metricsId = value;
            else
                metricsId = metricsId + "!$" + value;

            addCharts(value, text);
            deleteCookie(COOKIE_NAME);
            setCookie(metricsId);
        }
    }
}

function deleteSeries() {
    for (i=0; i<=chart.series.length; i++) {
       chart.series[1].remove(false);
    }
    deleteCookie(COOKIE_NAME);
    metricsId = "";
}

function hideInputElement(element) {
    if (element && element instanceof HTMLElement) {
        element.style.display = 'none'; // Hide the element
    }
}

function showInputElement(element) {
    if (element && element instanceof HTMLElement) {
        console.log(element);
        element.style.display = 'block'; // Restore default display (e.g., 'block' or 'inline')
    }
}

function convertStringToDate(dateString) {
    const dateObject = new Date(Date.parse(dateString));

    return dateObject;
}

function timeConverter(UNIX_timestamp){
    var a = new Date(UNIX_timestamp);
    var year = a.getFullYear();
    var month = a.getMonth();
    var date = a.getDate();
    var time = date + ' ' + month + ' ' + year;

    return time;
}
