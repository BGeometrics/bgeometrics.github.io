/**
 */
  var names = [
    { name: "Bitcoin Price USD", link: "reports/bitcoin_price_usd_g.html" },
    { name: "Bitcoin Realized Price", link: "reports/bitcoin_realized_price_g.html" },
    { name: "SOPR (Spent Output Profit Ratio)", link: "reports/bitcoin_charts_g_sopr.html" },
    { name: "Day moving average", link: "reports/bitcoin_200_moving_average_g.html" },
    { name: "NUPL (Net Unrealized Profit / Loss)", link: "reports/bitcoin_nupl_g.html" },
    { name: "Hodl Waves Realized Cap", link: "reports/bitcoin_reacap_hodl_waves_g.html" },
    { name: "Short Term Hodler Realized Price", link: "reports/bitcoin_realized_short_g.html" },
    { name: "Bitcoin Coin Destroyed Days Terminal Adjusted 90d", link: "reports/bitcoin_cdd_ajusted_90dma_g.html" },
    { name: "Hodl Waves", link: "reports/bitcoin_hodl_waves_relative_g.html" },
    { name: "Change BTC on exchanges", link: "reports/bitcoin_ex_change_held_g.html" },
    { name: "Bitcoin Fear and Greed", link: "reports/bitcoin_fear_greed_g.html" },
    { name: "AVIV (Asset Value to Investor Value) Ratio", link: "reports/bitcoin_aviv_g.html" },
    { name: "Bitcoin Halving Cycle", link: "reports/bitcoin_halving_cycle_g.html" },
    { name: "BTC price history and halving timeline", link: "reports/bitcoin_price_g_log.html" },
    { name: "Bitcoin Halving Radar", link: "reports/bitcoin_halving_radar_g.html" },
    { name: "Bitcoin Years Candles", link: "reports/bitcoin_year_candle_g.html" },
    { name: "Influence of the halving on the monthly price of bitcoin", link: "reports/bitcoin_halving_month_g.html" },
    { name: "", link: "" },
    { name: "", link: "" },
    { name: "", link: "" },
    { name: "", link: "" },
    { name: "", link: "" },
    { name: "", link: "" },
    { name: "", link: "" }
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
        resultsContainer.innerHTML += '<li><a href="' + results[j].link + '">' + results[j].name + '</a></li>';
      }

      resultsContainer.innerHTML += '</ul></br>';
    }
  }