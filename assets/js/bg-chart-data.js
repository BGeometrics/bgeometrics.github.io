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

// Devuelve la serie en formato Highcharts [[tsMs, val], ...].
// slug      : metrica en la API (p.ej. 'aviv', 'cdd', 'btc-price').
// staticUrl : URL del JSON estatico recortado (fallback para no suscriptores o error).
async function bgSeries(slug, staticUrl) {
    if (bgIsSubscriber()) {
        try {
            const rows = await fetch('https://api.bgeometrics.com/chart/' + slug, {
                credentials: 'include'
            }).then(r => r.json());
            if (Array.isArray(rows) && rows.length) {
                const k = Object.keys(rows[0]).find(x => x !== 'd' && x !== 'unixTs');
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
