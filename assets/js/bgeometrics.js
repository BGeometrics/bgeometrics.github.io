/**
 */
  var names = [
    { name: "Bitcoin Price USD", link: "reports/bitcoin_price_usd_g.html" },
    { name: "Bitcoin Capitalization", link: "graphics/capitalization.html" },
    { name: "Bitcoin Realized Capitalization", link: "graphics/capitalization.html" },
    { name: "Bitcoin Investor Capitalization", link: "graphics/capitalization.html" },
    { name: "Bitcoin Thermo Capitalization", link: "graphics/capitalization.html" },
    { name: "Bitcoin MVRV (Market Value Realized Price)", link: "graphics/mvrv.html" },
    { name: "Bitcoin MVRV Z-Score", link: "graphics/mvrv.html" },
    { name: "MVRV, LTH (Long Term Hodler) and STH (Short Term Hodler)", link: "graphics/mvrv.html" },
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
    { name: "Bitcoin Coin and Address Distribution", link: "reports/bitcoin_distribution_tables.html" },
    { name: "Bitcoin Distribution Coin", link: "reports/bitcoin_distribution_coin_g.html" },
    { name: "Whale Accumulation Heat Map", link: "reports/bitcoin_whale_accumulation_heatmap_g.html" },
    { name: "Bitcoin distribution Humpback >10K", link: "reports/bitcoin_distribution_coin_g_humpback.html" },
    { name: "Bitcoin distribution Whale 1000-10K", link: "reports/bitcoin_distribution_coin_g_whale.html" },
    { name: "Whale (1K-10K) Net Position BTC in 30d", link: "reports/bitcoin_whale_30d_sum_g.html" },
    { name: "Shark (100-1000) Net Position BTC 30d", link: "reports/bitcoin_shark_30d_sum_g.html" },
    { name: "MVRV Z-Score", link: "reports/bitcoin_mvrv_zscore_g.html" },
    { name: "Bitcoin realized price distribution (URPD)", link: "reports/bitcoin_price_histogram_g.html" },
    { name: "History bitcoin price on a day like today", link: "reports/bitcoin_price_usd_day_g.html" },
    { name: "Bitcoin Volatility", link: "reports/bitcoin_volatility_g.html" },
    { name: "Bitcoin S&P 500 correlation", link: "reports/bitcoin_sp500_correlation_g.html" },
    { name: "Bitcoin Dominance", link: "reports/bitcoin_dominance_g.html" },
    { name: "Bitcoin Daily Price Performance", link: "reports/bitcoin_daily_price_performance_g.html" },
    { name: "Bitcoin Liveniness", link: "reports/bitcoin_liveliness_g.html" },
    { name: "Long Term Hodler vs Short Term Hodler", link: "reports/bitcoin_lth_sth_g.html" },
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