/*
 * bg-chart-data.js — carga de series para las graficas con gating de historico.
 *
 * No suscriptores (anonimo / FREE): usan el JSON estatico de GitHub Pages, que ya
 * viene recortado en origen (ultimos 4 anos, embargo de la ultima semana).
 * Suscriptores de pago: la cookie legible `bg_full=1` (la emite BGUser en el login
 * solo para tiers de pago) hace que la grafica consulte la API /chart/<slug>, que
 * devuelve el historico completo (autorizado server-side por la cookie HttpOnly
 * `bg_token`). `bg_full` es solo una pista de UI; la autorizacion real la enforce
 * el backend, asi que falsearla no da acceso.
 */

function bgIsSubscriber() {
    return document.cookie.split('; ').indexOf('bg_full=1') !== -1;
}

// Cache en memoria: una sola promesa compartida por slug durante la carga de
// la pagina, para no repetir N fetches identicos a /chart/<slug> cuando varias
// series (p.ej. los 21 paises de m2-bank) provienen del mismo endpoint.
const _bgChartRowsCache = {};

function _bgFetchChartRows(slug) {
    if (!_bgChartRowsCache[slug]) {
        _bgChartRowsCache[slug] = fetch('https://api.bgeometrics.com/chart/' + slug, {
            credentials: 'include'
        }).then(r => r.json());
    }
    return _bgChartRowsCache[slug];
}

// Devuelve la serie en formato Highcharts [[tsMs, val], ...].
// slug      : metrica en la API (p.ej. 'aviv', 'cdd', 'btc-price', 'm2-bank').
// staticUrl : URL del JSON estatico recortado (fallback para no suscriptores o error).
// field     : opcional. Campo a extraer de la respuesta cuando el endpoint
//             devuelve varios campos ademas de d/unixTs (p.ej. 'usm2d' en
//             /chart/m2-bank). Si se omite, se autodetecta el primer campo
//             que no sea 'd' ni 'unixTs' (comportamiento igual que antes).
async function bgSeries(slug, staticUrl, field) {
    if (bgIsSubscriber()) {
        try {
            const rows = await _bgFetchChartRows(slug);
            if (Array.isArray(rows) && rows.length) {
                const k = field || Object.keys(rows[0]).find(x => x !== 'd' && x !== 'unixTs');
                return rows.map(o => [
                    Number(o.unixTs) * 1000,
                    o[k] == null ? null : Number(o[k])
                ]);
            }
        } catch (e) {
            /* cae al JSON estatico */
        }
    }
    return fetch(staticUrl).then(r => r.json());
}

// Media movil de `window` puntos sobre una serie [[tsMs, val], ...] ya resuelta
// (tipicamente el resultado de bgSeries). Se usa para derivar en el cliente
// metricas como el MVRV 365D MA a partir del historico completo del suscriptor,
// sin depender de un JSON estatico recortado ni de un endpoint dedicado.
// Replica pandas .rolling(window).mean(): null mientras no haya `window` puntos.
function bgRollingMean(series, window) {
    const result = [];
    const buffer = [];
    let sum = 0;

    for (const [ts, val] of series) {
        if (val == null) {
            result.push([ts, null]);
            continue;
        }
        buffer.push(val);
        sum += val;
        if (buffer.length > window) {
            sum -= buffer.shift();
        }
        result.push([ts, buffer.length === window ? sum / window : null]);
    }

    return result;
}

// Resta punto a punto dos series [[tsMs, val], ...] alineadas por indice
// (mismo origen y misma longitud, p.ej. mvrv menos su propio rolling mean).
function bgDiffSeries(seriesA, seriesB) {
    return seriesA.map(([ts, val], i) => {
        const other = seriesB[i] ? seriesB[i][1] : null;
        return [ts, (val == null || other == null) ? null : val - other];
    });
}
