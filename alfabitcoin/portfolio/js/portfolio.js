const API_BASE_URL = "https://portafolio.alfabitcoin.io";
//const API_BASE_URL = "";

function addRow() {
    // Añadir una nueva fila a la tabla de portafolio
    const row = `
                <tr>
                    <td class="asset-column">
                        <input 
                            id='asset-name' 
                            type="text" 
                            class="form-control bg-dark text-light" 
                            placeholder="Ej: Tesla, Inc." 
                            value="Ej: Tesla, Inc."
                            onfocus="if (this.value=='Ej: Tesla, Inc.') this.value = ''" 
                            onblur="if (this.value=='') { this.value = 'Ej: Tesla, Inc.'; copyToName(this); }"
                            onchange="copyToName(this)"
                        >
                    </td>
                    <td>
                        <input 
                            id="asset-symbol" 
                            type="text" 
                            class="form-control bg-dark text-light" 
                            placeholder="Ej: TSLA" 
                            value="Ej: TSLA"
                            onfocus="if (this.value=='Ej: TSLA') this.value = ''" 
                            onblur="if (this.value=='') { this.value = 'Ej: TSLA'; copyToAsset(this); }"
                            onchange="copyToAsset(this)"
                        >
                    </td>
                    <td><input type="number" class="form-control weight-input bg-dark text-light" placeholder="%" onchange="updateTotalWeight()"></td>
                    <td><button class="btn btn-danger btn-sm" onclick="removeRow(this)">X</button></td>
                </tr>`;
    document.getElementById("portfolio-body").insertAdjacentHTML('beforeend', row);
    updateTotalWeight();
    toggleReweightButton();
}

function removeRow(button) {
    // Remove the selected row from the portfolio table
    button.closest('tr').remove();
    updateTotalWeight();
    toggleReweightButton();
}

function updateTotalWeight() {
    // Calcular y actualizar el peso total del portafolio
    const weights = document.querySelectorAll('.weight-input');
    let total = 0;
    weights.forEach(input => {
        total += parseFloat(input.value) || 0;
    });

    // Formatear sin decimales
    document.getElementById("totalWeight").textContent = total.toFixed(0) + "%";
}

function copyToAsset(input) {
    input.value = input.value.toUpperCase().trim(); // Convertir a mayúsculas y eliminar espacios en blanco
    const symbol = input.value;

    // Realizar una solicitud GET al endpoint /asset con el símbolo
    fetch(`${API_BASE_URL}/public/asset?symbol=${symbol}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al recuperar el activo.");
            }
            let ret = response.text();

            return ret;
        })
        .then(asset => {
            // Eliminar las comillas del principio y del final de la respuesta
            asset = asset.replace(/^"|"$/g, '');
            asset = asset.slice(0, -2);

            // Actualizar la columna "Activo" con el nombre del activo recuperado
            const row = input.closest('tr');
            const assetCell = row.querySelector('.asset-column');

            if (asset) {
                assetCell.textContent = asset; // Asignar el texto recibido
            } else {
                assetCell.textContent = "Activo no encontrado";
            }

            // Poner el foco en el campo input type="number"
            const weightInput = row.querySelector('input[type="number"]');
            weightInput.focus();

            // Mostrar los paneles
            showPanels();
        })
        .catch(error => {
            console.error("Error:", error);
            showAlert("No se pudo recuperar el activo. Intente nuevamente.");
        });
}

function copyToName(input) {
    const name = input.value;
    const row = input.closest('tr');

    // Realizar una solicitud GET al endpoint /asset con el símbolo
    fetch(`${API_BASE_URL}/public/assetname?name=${name}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al recuperar el activo.");
            }

            return response.json(); // Cambiar a .json() para manejar la respuesta como JSON
        })
        .then(data => {
            //console.log("Datos recibidos:", data);

            const shortName = data[0];
            const symbol = data[1];

            if (symbol !== null) {
                console.log("Nombre corto:", symbol);
                // Actualizar la columna "Activo" con el nombre del activo recuperado
                const assetCell = row.querySelector('.asset-column');
                assetCell.textContent = shortName; // Asignar el nombre corto recibido

                // Actualizar la columna "Símbolo" con el símbolo recuperado
                const symbolInput = row.querySelector('input[type="text"]');
                symbolInput.value = symbol; // Asignar el símbolo recibido

                // Poner el foco en el campo input type="number"
                const weightInput = row.querySelector('input[type="number"]');
                weightInput.focus();

                showPanels();
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function showPanels() {
    document.getElementById("period").style.display = "block";
    document.getElementById("options").style.display = "block";
    document.getElementById("analytic").style.display = "block";
}

function toggleReweightButton() {
    // Show or hide the "Rebalance" button based on the number of rows
    const rows = document.querySelectorAll("#portfolio-body tr");
    const reweightButton = document.getElementById("reweight");
    if (rows.length >= 2) {
        reweightButton.style.display = "inline-block";
    } else {
        reweightButton.style.display = "none";
    }
}

function rebalanceWeights() {
    // Recalculate weights to ensure they sum up to 100% while maintaining proportions
    const weightInputs = document.querySelectorAll('.weight-input');
    let totalWeight = 0;

    // Sum all current weights
    weightInputs.forEach(input => {
        totalWeight += parseFloat(input.value) || 0;
    });

    // Recalculate weights to sum up to 100%
    weightInputs.forEach(input => {
        const currentWeight = parseFloat(input.value) || 0;
        const newWeight = (currentWeight / totalWeight) * 100;
        input.value = newWeight.toFixed(2); // Round to 2 decimals
    });

    updateTotalWeight();
}

function handleOtherChange() {
    // Show or hide the custom input field based on the selected option
    const otherSelect = document.getElementById("otherSelect");
    const customOther = document.getElementById("customOther");

    // Verificar si la opción "Otro" está seleccionada
    const selectedOptions = Array.from(otherSelect.selectedOptions).map(option => option.value);
    if (selectedOptions.includes("other")) {
        customOther.style.display = "block";
    } else {
        customOther.style.display = "none";
        customOther.value = "";
    }
}

function analyzePortfolio() {
    const analyzeButton = document.querySelector('button[onclick="analyzePortfolio()"]');
    analyzeButton.disabled = true;

    document.getElementById("portfolioStatistics").style.display = "none";
    document.getElementById("portfolioOptimizationGraphics").style.display = "none";
    document.getElementById("portfolioOptimizationGraphicsHead").style.display = "none";
    document.getElementById("portfolioOptimizedMetrics").style.display = "none";

    // Check if the total weight is 100% o cercano antes de analizar
    const totalWeight = parseFloat(document.getElementById("totalWeight").textContent);

    if (totalWeight <= 100.1 && totalWeight >= 99.9) {
        // Obtener los valores de las columnas "symbol" y "weight" de la tabla assets
        const symbols = [];
        const weights = [];
        document.querySelectorAll("#portfolio-body tr").forEach(row => {
            const symbol = row.querySelector('input[type="text"]').value;
            const weight = row.querySelector('input[type="number"]').value / 100;
            if (symbol && weight) {
                symbols.push(symbol);
                weights.push(weight);
            }
        });

        // Obtener el valor de timePeriodSelect
        const timePeriodSelect = document.getElementById("timePeriodSelect").value;

        // Crear un objeto con los parámetros
        const params = {
            symbols: symbols,
            weights: weights,
            percentageBTC: [0, 1, 5, 10, 25],
            timePeriodSelect: timePeriodSelect
        };

        // Cambiar el cursor a "wait"
        document.body.style.cursor = "wait";

        
        fetch(`${API_BASE_URL}/public/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al obtener los datos del servidor.");
                }
                return response.json();
            })
            .then(data => {
                // Acceder al array de datos dentro de "data"
                const portfolioSymbolsLate = data.symbols_late; // Segundo elemento del array "data"
                const portfolioData = data.data; // Primer elemento del array "data"

                // Mostrar alerta si hay símbolos que empiezan más tarde
                if (portfolioSymbolsLate && portfolioSymbolsLate.length > 0) {
                    const firstLate = portfolioSymbolsLate[0];
                    const formattedDate = formatDateToDDMMYYYY(firstLate[1]);
                    getAsset(firstLate[0]).then(asset => {
                        const msg = `El activo ${asset} (${firstLate[0]}) sólo tiene datos desde ${formattedDate}.`;
                        showAlert(msg);
                    });
                }
                else {
                    // Seleccionar el cuerpo de la tabla
                    const tableBody = document.querySelector("#portfolioStatistics tbody");
                    tableBody.innerHTML = ""; // Limpiar la tabla antes de insertar nuevos datos

                    // Insertar los datos recibidos en la tabla
                    portfolioData.forEach(row => {
                        const tableRow = `
                        <tr>
                            <td>${row.name}</td>
                            <td class="absolute-return">${row.absoluteReturn}</td>
                            <td class="volatility">${row.volatility}</td>
                            <td class="max-drawdown">${row.maxDrawdown}</td>
                            <td class="sharpe-ratio">${row.sharpeRatio}</td>
                            <td class="sortino-ratio">${row.sortinoRatio}</td>
                        </tr>
                    `;
                        tableBody.insertAdjacentHTML("beforeend", tableRow);
                    });

                    // Resaltar las métricas más importantes
                    highlightBestMetrics();

                    document.getElementById("portfolioStatistics").style.display = "block";
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showAlert("Hubo un problema al analizar el portafolio. Por favor, inténtelo nuevamente.");
            })
            .finally(() => {
                document.body.style.cursor = "default";
                analyzeButton.disabled = false;
            });

    } else {
        showAlert("Para analizar el portafolio el total de los pesos debe ser del 100%.");
        analyzeButton.disabled = false;
    }
}

function highlightBestMetrics() {
    // Resaltar las mejores métricas en la tabla
    let maxAbsoluteReturn = -Infinity;
    let maxAbsoluteReturnCell = null;

    let minVolatility = Infinity;
    let minVolatilityCell = null;

    let minMaxDrawdown = Infinity;
    let minMaxDrawdownCell = null;

    let maxSharpeRatio = -Infinity;
    let maxSharpeRatioCell = null;

    let maxSortinoRatio = -Infinity;
    let maxSortinoRatioCell = null;

    // Buscar las celdas con los mejores valores
    document.querySelectorAll(".absolute-return").forEach(cell => {
        const value = parseFloat(cell.textContent.replace("%", ""));
        if (value > maxAbsoluteReturn) {
            maxAbsoluteReturn = value;
            maxAbsoluteReturnCell = cell;
        }
    });

    document.querySelectorAll(".volatility").forEach(cell => {
        const value = parseFloat(cell.textContent.replace("%", ""));
        if (value < minVolatility) {
            minVolatility = value;
            minVolatilityCell = cell;
        }
    });

    document.querySelectorAll(".max-drawdown").forEach(cell => {
        const value = parseFloat(cell.textContent.replace("%", "").replace("-", ""));
        if (value < minMaxDrawdown) {
            minMaxDrawdown = value;
            minMaxDrawdownCell = cell;
        }
    });

    document.querySelectorAll(".sharpe-ratio").forEach(cell => {
        const value = parseFloat(cell.textContent);
        if (value > maxSharpeRatio) {
            maxSharpeRatio = value;
            maxSharpeRatioCell = cell;
        }
    });

    document.querySelectorAll(".sortino-ratio").forEach(cell => {
        const value = parseFloat(cell.textContent);
        if (value > maxSortinoRatio) {
            maxSortinoRatio = value;
            maxSortinoRatioCell = cell;
        }
    });

    // Aplicar estilos a las mejores métricas
    if (maxAbsoluteReturnCell) {
        maxAbsoluteReturnCell.style.backgroundColor = "#ff9800";
        maxAbsoluteReturnCell.style.color = "#fff";
    }
    if (minVolatilityCell) {
        minVolatilityCell.style.backgroundColor = "#ff9800";
        minVolatilityCell.style.color = "#fff";
    }
    if (minMaxDrawdownCell) {
        minMaxDrawdownCell.style.backgroundColor = "#ff9800";
        minMaxDrawdownCell.style.color = "#fff";
    }
    if (maxSharpeRatioCell) {
        maxSharpeRatioCell.style.backgroundColor = "#ff9800";
        maxSharpeRatioCell.style.color = "#fff";
    }
    if (maxSortinoRatioCell) {
        maxSortinoRatioCell.style.backgroundColor = "#ff9800";
        maxSortinoRatioCell.style.color = "#fff";
    }
}

function optimizePortfolioBTC() {
    const optimizeBTCButton = document.querySelector('button[onclick="optimizePortfolioBTC()"]');
    optimizeBTCButton.disabled = true;

    document.getElementById("portfolioStatistics").style.display = "none";
    document.getElementById("portfolioOptimizationGraphics").style.display = "none";
    document.getElementById("portfolioOptimizationGraphicsHead").style.display = "none";
    document.getElementById("portfolioOptimizedMetrics").style.display = "none";

    // Check if the total weight is 100% o cercano antes de analizar
    const totalWeight = parseFloat(document.getElementById("totalWeight").textContent);

    if (totalWeight <= 100.1 && totalWeight >= 99.9) {
        // Obtener los valores de las columnas "symbol" y "weight" de la tabla assets
        const assets = [];
        const symbols = [];
        const weights = [];
        let hasBTC = false;

        document.querySelectorAll("#portfolio-body tr").forEach(row => {
            const symbol = row.querySelector('input[type="text"]').value;
            const asset = row.querySelector('.asset-column').textContent;
            let weight = row.querySelector('input[type="number"]').value / 100;

            if (symbol && weight && asset) {
                // Comprobar si ya existe BTC-USD
                if (symbol === "BTC/USD") {
                    hasBTC = true;
                } else {
                    // Si no es BTC, ajustar el peso solo si no hay BTC
                    if (!hasBTC) {
                        weight = weight * 0.9; // Reducir al 90% solo si se va a añadir BTC
                    }
                }

                symbols.push(symbol);
                weights.push(weight);
                assets.push(asset);
            }
        });

        // Añadir BTC/USD solo si no existe ya
        if (!hasBTC) {
            symbols.push("BTC/USD");
            weights.push(0.1); // 10% para BTC
            assets.push("Bitcoin");
        }

        // Obtener el valor de timePeriodSelect
        const timePeriodSelect = document.getElementById("timePeriodSelect").value;

        // Crear un objeto con los parámetros
        const params = {
            assets: assets,
            symbols: symbols,
            weights: weights,
            percentageBTC: [0, 1, 5, 10, 25],
            timePeriodSelect: timePeriodSelect
        };

        document.body.style.cursor = "wait";

        // Realizar la solicitud al servidor
        fetch(`${API_BASE_URL}/public/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al obtener los datos del servidor.");
                }
                return response.json();
            })
            .then(data => {
                const portfolioData = data.data; 
                const optimizedMetricsData = data.optimized_metrics;
                const portfolioSymbolsLate = data.symbols_late; // Segundo elemento del array "data"
               
                // Mostrar alerta si hay símbolos que empiezan más tarde
                if (portfolioSymbolsLate && portfolioSymbolsLate.length > 0) {
                    const firstLate = portfolioSymbolsLate[0];
                    const formattedDate = formatDateToDDMMYYYY(firstLate[1]);
                    getAsset(firstLate[0]).then(asset => {
                        const msg = `El activo ${asset} (${firstLate[0]}) sólo tiene datos desde ${formattedDate}.`;
                        showAlert(msg);
                    });
                }
                else { 
                    createGraphics(portfolioData);

                    const tableOptimizedMetrics = document.querySelector("#portfolioOptimizedMetricsTable tbody");
                    tableOptimizedMetrics.innerHTML = "";

                    optimizedMetricsData.forEach(row => {
                        const tableRow = `
                                    <tr>
                                        <td>${row.name}</td>
                                        <td>${row.absoluteReturn}</td>
                                        <td>${row.volatility}</td>
                                        <td>${row.maxDrawdown}</td>
                                        <td>${row.sharpeRatio}</td>
                                        <td>${row.sortinoRatio}</td>
                                    </tr>
                                `;
                        tableOptimizedMetrics.insertAdjacentHTML("beforeend", tableRow);
                    });

                    highlightBestOptimizedMetrics();
                    roundSharpeSortinoRatio();
                    document.getElementById("portfolioOptimizedMetrics").style.display = "block";
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showAlert("Hubo un problema al optimizar el portafolio. Por favor, inténtelo nuevamente.");
            })
            .finally(() => {
                document.body.style.cursor = "default";
                optimizeBTCButton.disabled = false;
            });

    } else {
        showAlert("Para optimizar el portafolio el total de los pesos debe ser del 100%.");
        optimizeBTCButton.disabled = false;
    }
}

function optimizePortfolio() {
    const optimizeButton = document.querySelector('button[onclick="optimizePortfolio()"]');
    optimizeButton.disabled = true;

    document.getElementById("portfolioStatistics").style.display = "none";
    document.getElementById("portfolioOptimizationGraphics").style.display = "none";
    document.getElementById("portfolioOptimizationGraphicsHead").style.display = "none";
    document.getElementById("portfolioOptimizedMetrics").style.display = "none";

    // Check if the total weight is 100% o cercano antes de analizar
    const totalWeight = parseFloat(document.getElementById("totalWeight").textContent);

    if (totalWeight <= 100.1 && totalWeight >= 99.9) {
        // Obtener los valores de las columnas "symbol" y "weight" de la tabla assets
        const assets = [];
        const symbols = [];
        const weights = [];
        document.querySelectorAll("#portfolio-body tr").forEach(row => {
            const symbol = row.querySelector('input[type="text"]').value;
            const weight = row.querySelector('input[type="number"]').value / 100;
            const asset = row.querySelector('.asset-column').textContent;

            if (symbol && weight && asset) {
                symbols.push(symbol);
                weights.push(weight);
                assets.push(asset);
            }
        });

        // Obtener el valor de timePeriodSelect
        const timePeriodSelect = document.getElementById("timePeriodSelect").value;

        // Crear un objeto con los parámetros
        const params = {
            assets: assets,
            symbols: symbols,
            weights: weights,
            percentageBTC: [0, 1, 5, 10, 25],
            timePeriodSelect: timePeriodSelect
        };

        // Cambiar el cursor a "wait"
        document.body.style.cursor = "wait";

        // Realizar la solicitud al servidor
        fetch(`${API_BASE_URL}/public/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Error al obtener los datos del servidor.");
                }
                return response.json();
            })
            .then(data => {
                const portfolioData = data.data; 
                const optimizedMetricsData = data.optimized_metrics;
                const portfolioSymbolsLate = data.symbols_late; // Segundo elemento del array "data"

                // Mostrar alerta si hay símbolos que empiezan más tarde
                if (portfolioSymbolsLate && portfolioSymbolsLate.length > 0) {
                    const firstLate = portfolioSymbolsLate[0];
                    const formattedDate = formatDateToDDMMYYYY(firstLate[1]);
                    getAsset(firstLate[0]).then(asset => {
                        const msg = `El activo ${asset} (${firstLate[0]}) sólo tiene datos desde ${formattedDate}.`;
                        showAlert(msg);
                    });
                }
                else { 
                    createGraphics(portfolioData);

                    const tableOptimizedMetrics = document.querySelector("#portfolioOptimizedMetricsTable tbody");
                    tableOptimizedMetrics.innerHTML = "";

                    optimizedMetricsData.forEach(row => {
                        const tableRow = `
                                    <tr>
                                        <td>${row.name}</td>
                                        <td>${row.absoluteReturn}</td>
                                        <td>${row.volatility}</td>
                                        <td>${row.maxDrawdown}</td>
                                        <td>${row.sharpeRatio}</td>
                                        <td>${row.sortinoRatio}</td>
                                    </tr>
                                `;
                        tableOptimizedMetrics.insertAdjacentHTML("beforeend", tableRow);
                    });

                    highlightBestOptimizedMetrics();
                    roundSharpeSortinoRatio();
                    document.getElementById("portfolioOptimizedMetrics").style.display = "block";
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showAlert("Hubo un problema al optimizar el portafolio. Por favor, inténtelo nuevamente.");
            })
            .finally(() => {
                document.body.style.cursor = "default";
                optimizeButton.disabled = false;
            });

    } else {
        showAlert("Para optimizar el portafolio el total de los pesos debe ser del 100%.");
        optimizeButton.disabled = false;
    }
}

function loadPortfolio(portfolioName) {
    // Cerrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('defaultPortfolioModal'));
    modal.hide();

    showPanels();

    // Limpiar la tabla actual
    document.getElementById("portfolio-body").innerHTML = "";

    // Datos de ejemplo para cada portafolio
    const portfolios = {
        "Permanent Portfolio": [
            { symbol: "GLD", asset: "SPDR Gold Trust", weight: 33.33 },
            { symbol: "ITOT", asset: "iShares Core S&P Total U.S. Sto", weight: 33.33 },
            //{ symbol: "BIL", asset: "SPDR Bloomberg 1-3 Month T-Bill", weight: 25 },
            { symbol: "VGLT", asset: "Vanguard Long-Treasury ETF", weight: 33.34 }
        ],
        "Multi-asset": [
            { symbol: "IEV", asset: "iShares Europe ETF", weight: 6.67 },
            { symbol: "VO", asset: "Vanguard Mid-Cap ETF", weight: 6.67 },
            { symbol: "VEA", asset: "Vanguard FTSE Developed Markets", weight: 6.67 },
            { symbol: "SPY", asset: "SPDR S&P 500", weight: 6.67 },
            { symbol: "VEU", asset: "Vanguard FTSE All World Ex US E", weight: 6.67 },
            { symbol: "VTI", asset: "Vanguard Total Stock Market ETF", weight: 6.67 },
            { symbol: "GSG", asset: "iShares GSCI Commodity-Indexed", weight: 6.67 },
            { symbol: "KBE", asset: "SPDR S&P Bank ETF", weight: 6.67 },
            { symbol: "VNQ", asset: "Vanguard Real Estate ETF", weight: 6.67 },
            { symbol: "SLV", asset: "iShares Silver Trust", weight: 6.67 },
            { symbol: "ACWI", asset: "iShares MSCI ACWI ETF", weight: 6.66 },
            { symbol: "GLD", asset: "SPDR Gold Trust", weight: 6.66 },
            { symbol: "HYG", asset: "iShares iBoxx High Yield Corp", weight: 6.66 },
            { symbol: "TLT", asset: "iShares 20+ Year Treasury Bond", weight: 6.66 },
            { symbol: "QQQ", asset: "Invesco QQQ Trust", weight: 6.66 },
        ],
        "Diversified Bond": [
            { symbol: "IEF", asset: "iShares 7-10 Year Treasury Bond ETF", weight: 20 },
            { symbol: "JNK", asset: "SPDR Bloomberg High Yield Bond ETF", weight: 20 },
            { symbol: "VIG", asset: "Vanguard Dividend A...reciation Index Fund", weight: 20 },
            { symbol: "TLT", asset: "iShares 20+ Year Treasury Bond ETF", weight: 20 },
            { symbol: "HYG", asset: "iShares iBoxx $ Hig...d Corporate Bond ETF", weight: 20 },
        ],
        "All Seasons": [
            { symbol: "VGLT", asset: "Long Term Bonds", weight: 43 },
            { symbol: "ITOT", asset: "Total Stock Market", weight: 33 },
            { symbol: "VGIT", asset: "Intermediate Bonds", weight: 13 },
            //{ symbol: "GSP", asset: "Commodities", weight: 7.5 }, // No está incluida en la API
            { symbol: "GLD", asset: "Gold", weight: 11 },
        ],
        "Clasic 60/40": [
            { symbol: "SPY", asset: "SPDR S&P 500", weight: 60 },
            { symbol: "BND", asset: "Vanguard Total Bond Market ETF", weight: 40 },
        ]
    };

    // Cargar el portafolio seleccionado
    const selectedPortfolio = portfolios[portfolioName];
    selectedPortfolio.forEach(item => {
        const row = `
                    <tr>
                        <td class="asset-column">${item.asset}</td>
                        <td><input id="asset-symbol" type="text" class="form-control bg-dark text-light" value="${item.symbol}" onblur="copyToAsset(this)"></td>
                        <td><input type="number" class="form-control bg-dark text-light weight-input" value="${item.weight}" onchange="updateTotalWeight()"></td>
                        <td><button class="btn btn-danger btn-sm" onclick="removeRow(this)">X</button></td>
                    </tr>`;
        document.getElementById("portfolio-body").insertAdjacentHTML('beforeend', row);
    });

    // Actualizar el peso total y mostrar el botón de rebalanceo si es necesario
    updateTotalWeight();
    toggleReweightButton();
}

// Initialize Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function () {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

function showAlert(message) {
    document.getElementById("alertMessage").textContent = message;

    const alertModal = new bootstrap.Modal(document.getElementById("alertModal"));
    alertModal.show();
}

function loadPortfolioOptimizationData() {
    document.getElementById("portfolioOptimization").style.display = "block";
    // Datos de prueba
    const testData = [
        { name: "GLD", composition: "20%", volatility: "8%", minDrawdown: "12%", sharpeRatio: "10%", sortinoRatio: "17%" },
        { name: "AAPL", composition: "10%", volatility: "12%", minDrawdown: "20%", sharpeRatio: "20%", sortinoRatio: "3%" },
        { name: "TSLA", composition: "30%", volatility: "39%", minDrawdown: "8%", sharpeRatio: "50%", sortinoRatio: "31%" },
        { name: "BTC", composition: "40%", volatility: "41%", minDrawdown: "60%", sharpeRatio: "20%", sortinoRatio: "49%" },
        { name: "Portafolio optimizado", composition: "", volatility: "10%", minDrawdown: "5%", sharpeRatio: "13%", sortinoRatio: "4%" },
    ];

    // Seleccionar el cuerpo de la tabla
    const tableBody = document.querySelector("#portfolioOptimization tbody");
    tableBody.innerHTML = "";

    // Insertar los datos de prueba en la tabla
    testData.forEach(row => {
        const tableRow = `
                    <tr>
                        <td>${row.name}</td>
                        <td>${row.composition}</td>
                        <td>${row.volatility}</td>
                        <td>${row.minDrawdown}</td>
                        <td>${row.sharpeRatio}</td>
                        <td>${row.sortinoRatio}</td>
                    </tr>
                `;
        tableBody.insertAdjacentHTML("beforeend", tableRow);
    });
}

// Create pie chart for assets and metrics
function createGraphics(portfolioData) {
    const filteredData = portfolioData.filter(asset => asset.name !== 'Rentabilidad anualizada');

    const volatilityChartData = filteredData.map(asset => ({
        name: asset.name,
        y: parseFloat(asset.volatility.replace('%', ''))
    }));

    const drawdownChartData = filteredData.map(asset => ({
        name: asset.name,
        y: Math.abs(parseFloat(asset.minDrawdown.replace('%', '')))
    }));

    // Crear contenedor para los gráficos
    const chartsContainer = document.getElementById('portfolioOptimizationGraphics');
    chartsContainer.innerHTML = `
    <div class="row mb-4">
        <h4>Resultados de la optimización</h4>
        <div class="col-md-6" id="volatilityChart" style="border: 2px solid white; padding: 10px;"></div>
        <div class="col-md-6" id="drawdownChart" style="border: 2px solid white; padding: 10px;"></div>
        <div class="col-md-6" id="sharpeChart" style="border: 2px solid white; padding: 10px;"></div>
        <div class="col-md-6" id="sortinoChart" style="border: 2px solid white; padding: 10px;"></div>
    </div>
`;

    try {
        // Gráfico de volatilidad
        Highcharts.chart('volatilityChart', {
            chart: {
                type: 'pie',
                backgroundColor: 'transparent',
                height: '350px'
            },
            title: {
                useHTML: true,
                text: 'Portafolio para Minimizar Volatilidad <i class="bi bi-info-circle" title="Busca la menor variación posible en los rendimientos. Ideal para inversores muy conservadores que priorizan estabilidad."></i>',
                style: {
                    color: '#ffffff'
                }
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: '#ffffff'
                        }
                    }
                }
            },
            series: [{
                name: 'Volatilidad',
                colorByPoint: true,
                data: volatilityChartData
            }],
            credits: {
                enabled: false
            }
        });

        // Gráfico de drawdown
        Highcharts.chart('drawdownChart', {
            chart: {
                type: 'pie',
                backgroundColor: 'transparent',
                height: '350px'
            },
            title: {
                useHTML: true,
                text: 'Portafolio para Minimizar Drawdown <i class="bi bi-info-circle" title="Reduce la mayor caída desde un máximo hasta un mínimo (pérdida máxima desde un pico). Protege mejor frente a caídas grandes del mercado."></i>',
                style: {
                    color: '#ffffff'
                }
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: '#ffffff'
                        }
                    }
                }
            },
            series: [{
                name: 'Drawdown',
                colorByPoint: true,
                data: drawdownChartData
            }],
            credits: {
                enabled: false
            }
        });

        // Crear datos para los nuevos gráficos
        const sharpeChartData = filteredData.map(asset => ({
            name: asset.name,
            y: parseFloat(asset.sharpeRatio.replace('%', ''))
        }));

        const sortinoChartData = filteredData.map(asset => ({
            name: asset.name,
            y: parseFloat(asset.sortinoRatio.replace('%', ''))
        }));

        // Gráfico de Sharpe Ratio
        Highcharts.chart('sharpeChart', {
            chart: {
                type: 'pie',
                backgroundColor: 'transparent',
                height: '350px'
            },
            title: {
                useHTML: true,
                text: 'Portafolio para Maximizar Sharpe Ratio <i class="bi bi-info-circle" title="Busca el mejor rendimiento ajustado por riesgo total (volatilidad). Usa una tasa libre de riesgo del 2% como referencia."></i><br><small>(rf=2%)</small>',
                style: {
                    color: '#ffffff'
                }
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: '#ffffff'
                        }
                    }
                }
            },
            series: [{
                name: 'Sharpe Ratio',
                colorByPoint: true,
                data: sharpeChartData
            }],
            credits: {
                enabled: false
            }
        });

        // Gráfico de Sortino Ratio
        Highcharts.chart('sortinoChart', {
            chart: {
                type: 'pie',
                backgroundColor: 'transparent',
                height: '350px'
            },
            title: {
                useHTML: true,
                text: 'Portafolio para Maximizar Sortino Ratio <i class="bi bi-info-circle" title="Similar al Sharpe, pero sólo penaliza la volatilidad negativa (pérdidas). Más adecuado si sólo te preocupan las caídas y no las subidas."></i><br><small>(rf=2%)</small>',
                style: {
                    color: '#ffffff'
                }
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: '#ffffff'
                        }
                    }
                }
            },
            series: [{
                name: 'Sortino Ratio',
                colorByPoint: true,
                data: sortinoChartData
            }],

            credits: {
                enabled: false
            },
        });

        chartsContainer.style.display = 'block';
    } catch (error) {
        console.error("Error al crear los gráficos:", error);
    }
}

function highlightBestOptimizedMetrics() {
    const table = document.getElementById("portfolioOptimizedMetricsTable");
    const rows = Array.from(table.getElementsByTagName("tr")).slice(1); // Skip header row

    let minVolCell = null;
    let minMaxDrawdownCell = null;
    let maxSharpeRatioCell = null;
    let maxSortinoRatioCell = null;
    let maxReturnCell = null;

    let minVol = Infinity;
    let minDrawdown = -Infinity;
    let maxSharpe = -Infinity;
    let maxSortino = -Infinity;
    let maxReturn = -Infinity;

    // Find best metrics
    rows.forEach(row => {
        const cells = row.getElementsByTagName("td");
        if (cells.length >= 6) {
            const returnValue = parseFloat(cells[1].textContent.replace('%', ''));
            const volValue = parseFloat(cells[2].textContent.replace('%', ''));
            const drawdownValue = parseFloat(cells[3].textContent.replace('%', ''));
            const sharpeValue = parseFloat(cells[4].textContent);
            const sortinoValue = parseFloat(cells[5].textContent);

            if (volValue < minVol) {
                minVol = volValue;
                minVolCell = cells[2];
            }
            if (drawdownValue > minDrawdown) {
                minDrawdown = drawdownValue;
                minMaxDrawdownCell = cells[3];
            }
            if (sharpeValue > maxSharpe) {
                maxSharpe = sharpeValue;
                maxSharpeRatioCell = cells[4];
            }
            if (sortinoValue > maxSortino) {
                maxSortino = sortinoValue;
                maxSortinoRatioCell = cells[5];
            }
            if (returnValue > maxReturn) {
                maxReturn = returnValue;
                maxReturnCell = cells[1];
            }
        }
    });

    // Reset all cell styles
    rows.forEach(row => {
        Array.from(row.getElementsByTagName("td")).forEach(cell => {
            cell.style.backgroundColor = "";
            cell.style.color = "";
        });
    });

    // Highlight best metrics
    if (minVolCell) {
        minVolCell.style.backgroundColor = "#ff9800";
        minVolCell.style.color = "#fff";
    }
    if (minMaxDrawdownCell) {
        minMaxDrawdownCell.style.backgroundColor = "#ff9800";
        minMaxDrawdownCell.style.color = "#fff";
    }
    if (maxSharpeRatioCell) {
        maxSharpeRatioCell.style.backgroundColor = "#ff9800";
        maxSharpeRatioCell.style.color = "#fff";
    }
    if (maxSortinoRatioCell) {
        maxSortinoRatioCell.style.backgroundColor = "#ff9800";
        maxSortinoRatioCell.style.color = "#fff";
    }
    if (maxReturnCell) {
        maxReturnCell.style.backgroundColor = "#ff9800";
        maxReturnCell.style.color = "#fff";
    }
}

/* A rounding. In some cases, non-convexity may occur in the results. */
function roundSharpeSortinoRatio() {
    const table = document.getElementById("portfolioOptimizedMetricsTable");
    if (!table) return;

    let sharpeRow = null;
    let sortinoRow = null;

    // Buscar las filas correspondientes
    Array.from(table.getElementsByTagName("tr")).forEach(row => {
        const cells = row.getElementsByTagName("td");
        if (cells.length > 0) {
            if (cells[0].textContent.includes("Maximizar Sharpe Ratio")) {
                sharpeRow = row;
            }
            if (cells[0].textContent.includes("Maximizar Sortino Ratio")) {
                sortinoRow = row;
            }
        }
    });

    if (sharpeRow && sortinoRow) {
        const sharpeSortinoCell = sharpeRow.getElementsByTagName("td")[5];
        const sortinoSortinoCell = sortinoRow.getElementsByTagName("td")[5];

        const sharpeSortinoValue = parseFloat(sharpeSortinoCell.textContent);
        const sortinoSortinoValue = parseFloat(sortinoSortinoCell.textContent);

        if (sharpeSortinoValue > sortinoSortinoValue) {
            sortinoSortinoCell.textContent = sharpeSortinoCell.textContent;
            console.log("Rounding Sortino: " + sharpeSortinoValue + " (Sharpe's Sortino) > " + sortinoSortinoValue + " (Sortino's Sortino)");
        } 

        const sharpeSharpeCell = sharpeRow.getElementsByTagName("td")[4]; // Sharpe Ratio column for Sharpe portfolio
        const sortinoSharpeCell = sortinoRow.getElementsByTagName("td")[4]; // Sharpe Ratio column for Sortino portfolio

        const sharpeSharpeValue = parseFloat(sharpeSharpeCell.textContent);
        const sortinoSharpeValue = parseFloat(sortinoSharpeCell.textContent);

        if (sortinoSharpeValue > sharpeSharpeValue) {
            sharpeSharpeCell.textContent = sortinoSharpeCell.textContent;
            console.log("Rounding Sharpe: " + sortinoSharpeValue + " (Sortino's Sharpe) > " + sharpeSharpeValue + " (Sharpe's Sharpe)");
        }
    }
}

function roundSortinoRatio() {
    const table = document.getElementById("portfolioOptimizedMetricsTable");
    if (!table) return;

    let sharpeRow = null;
    let sortinoRow = null;

    // Buscar las filas correspondientes
    Array.from(table.getElementsByTagName("tr")).forEach(row => {
        const cells = row.getElementsByTagName("td");
        if (cells.length > 0) {
            if (cells[0].textContent.includes("Maximizar Sharpe Ratio")) {
                sharpeRow = row;
            }
            if (cells[0].textContent.includes("Maximizar Sortino Ratio")) {
                sortinoRow = row;
            }
        }
    });

    if (sharpeRow && sortinoRow) {
        const sharpeSortinoCell = sharpeRow.getElementsByTagName("td")[5];
        const sortinoSortinoCell = sortinoRow.getElementsByTagName("td")[5];

        const sharpeSortinoValue = parseFloat(sharpeSortinoCell.textContent);
        const sortinoSortinoValue = parseFloat(sortinoSortinoCell.textContent);
        console.log("Sharpe Sortino Value:", sharpeSortinoValue);
        console.log("Sortino Sortino Value:", sortinoSortinoValue);

        if (sharpeSortinoValue > sortinoSortinoValue) {
            sortinoSortinoCell.textContent = sharpeSortinoCell.textContent;
            console.log("Rounding " + sharpeSortinoValue + " - " + sortinoSortinoValue);
            // Opcional: resaltar el cambio
            //sortinoSortinoCell.style.backgroundColor = "#ff9800";
            //sortinoSortinoCell.style.color = "#fff";
        }
    }
}

async function getAsset(symbol) {
    try {
        const response = await fetch(`${API_BASE_URL}/public/asset?symbol=${symbol}`);
        if (!response.ok) {
            throw new Error("Error al recuperar el activo.");
        }
        let asset = await response.text();
        console.log("Asset response:", asset);
        asset = asset.replace(/^"|"$/g, '');
        asset = asset.slice(0, -2);

        return asset;
    } catch (error) {
        console.error("Error:", error);
        showAlert("No se pudo recuperar el activo. Intente nuevamente.");

        return null;
    }
}

function formatDateToDDMMYYYY(dateString) {
    const dateObj = new Date(dateString);
    const day = String(dateObj.getDate()).padStart(2, '0');
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const year = dateObj.getFullYear();

    return `${day}-${month}-${year}`;
}