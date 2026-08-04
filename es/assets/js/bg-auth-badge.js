/*
 * bg-auth-badge.js — indicador de sesion/suscripcion en la cabecera.
 *
 * Rellena el placeholder <li id="bg-auth-status"></li> con un badge que refleja si el
 * usuario tiene acceso al historico completo. Reutiliza bgIsSubscriber() de
 * bg-chart-data.js (la misma fuente de verdad que usa el gating de las graficas), de modo
 * que el badge y la banda naranja "Login / Upgrade" de los graficos nunca pueden discrepar.
 *
 * Nace porque hay suscriptores que ven las graficas recortadas (AVIV, M2...) sin darse
 * cuenta de que simplemente no han iniciado sesion en ese navegador.
 *
 * Limitacion conocida: la unica cookie legible por JS es `bg_full`, que BGUser solo emite
 * para tiers de pago activos (`bg_token` es HttpOnly). Un usuario FREE logado es por tanto
 * indistinguible de un anonimo, asi que el estado negativo dice "Log in / Upgrade" —
 * correcto en los tres casos (anonimo, FREE logado, suscriptor deslogado) — y nunca afirma
 * que la sesion este cerrada.
 */

(function () {

    var PORTAL = 'https://portal.bgeometrics.com';

    // color:#000000 explicito (no `inherit`): en el tema dark el color heredado es gris
    // claro y el texto quedaria ilegible sobre el fondo del badge.
    var PILL = 'display:inline-flex;align-items:center;gap:5px;' +
               'padding:4px 10px;border-radius:12px;font-size:12px;font-weight:bold;' +
               'color:#000000;text-decoration:none;white-space:nowrap;' +
               'box-shadow:0 1px 3px rgba(0,0,0,0.4);';

    // Para los <a> anidados dentro del pill: heredan el #000000 del contenedor.
    var LINK = 'color:inherit;text-decoration:none;';

    function render() {
        var host = document.getElementById('bg-auth-status');
        if (!host) {
            return; // pagina sin cabecera (p.ej. un grafico embebido) → no hace nada
        }

        var isSub = (typeof bgIsSubscriber === 'function') && bgIsSubscriber();
        var isEs = (document.documentElement.lang || '').toLowerCase().indexOf('es') === 0;

        if (isSub) {
            // El .html de este href va dentro del JS, no de la plantilla, asi que no lo
            // toca el replace('.html', '_dark.html') del generador de paginas.
            host.innerHTML =
                '<a href="' + PORTAL + '/dashboard.html" style="' + PILL +
                    'background:#10b981;" title="' +
                    (isEs ? 'Sesion iniciada — historico completo desbloqueado'
                          : 'Signed in — full history unlocked') + '">' +
                  '<i class="bi bi-patch-check-fill"></i>' +
                  '<span class="d-none d-md-inline">' +
                    (isEs ? 'Suscriptor' : 'Subscriber') +
                  '</span>' +
                '</a>';
            return;
        }

        // El icono es en si mismo el enlace de login: en movil el texto se oculta y el
        // badge queda reducido al candado, que debe seguir siendo pulsable.
        // Los dos textos van juntos en un unico hijo flex para que el separador " / "
        // no herede el `gap` del contenedor y quede pegado como en el pill verde.
        host.innerHTML =
            '<span style="' + PILL + 'background:#F7931A;" title="' +
                (isEs ? 'Historico limitado. Inicia sesion con tu suscripcion para verlo completo'
                      : 'Limited history. Log in with your subscription to see it in full') + '">' +
              '<a href="' + PORTAL + '/login" style="' + LINK + 'display:inline-flex;">' +
                '<i class="bi bi-lock-fill"></i>' +
              '</a>' +
              '<span class="d-none d-md-inline">' +
                '<a href="' + PORTAL + '/login" style="' + LINK + '">' +
                  (isEs ? 'Iniciar sesion' : 'Log in') +
                '</a> / ' +
                '<a href="' + PORTAL + '/pricing" style="' + LINK + '">' +
                  (isEs ? 'Mejorar' : 'Upgrade') +
                '</a>' +
              '</span>' +
            '</span>';
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', render);
    } else {
        render();
    }

})();
