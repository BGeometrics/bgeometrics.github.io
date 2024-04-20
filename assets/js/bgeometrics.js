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
    { name: "Short Term Hodler Realized Price", link: "reports/bitcoin_realized_short_g.html" },
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
    { name: "Bitcoin realized price distribution (URPD)", link: "reports/bitcoin_price_histogram_g.html" },
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

  /*
  function getMetric() {
      var e = document.getElementById("metrics");
      var value = e.value;
      var text = e.options[e.selectedIndex].text;
      var yAxis = 0;

      console.log(e.value);
      console.log(text);

      console.log(value.indexOf('_axis'));
      if (value.indexOf('_axis') > 0) {
          value = value.substring(0, value.indexOf('_axis'));
          yAxis = 1;
      }
      data = fetch('https://charts.bgeometrics.com/files/' + value + '.json')
          .then(response => response.json());

      Promise.all([data]).then(values => {
          chart.addSeries({
              id: value,
              name: text,
              data: values[0],
              tooltip: {
                  valueDecimals: 2
              },
              yAxis: yAxis
              
          });
      });
  }

  function getMetric2() {
      var e = document.getElementById("metrics");
      var value = e.value;
      var text = e.options[e.selectedIndex].text;
      var yAxis = 0;

      console.log(e.value);
      console.log(text);

      addCharts(e.value, text);
  }
*/

function addCharts(_metricId, _text){
    var e = document.getElementById("metrics");
    var text;
    var yAxis = 0;

    console.log(_metricId.indexOf('_axis'));
    if (_metricId.indexOf('_axis') > 0) {
        _metricId = _metricId.substring(0, _metricId.indexOf('_axis'));
        yAxis = 1;
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
    console.log("Set cookie " + cookieString + expires);

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
    console.log("Delete cookie " + name);
}

function changeMetrics() {
    var e = document.getElementById("metrics");
    var value = e.value;
    var text = e.options[e.selectedIndex].text;

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

function deleteSeries() {
    chart.series[1].remove(false);
    deleteCookie(COOKIE_NAME);
}
