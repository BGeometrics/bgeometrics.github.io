/*
 * bg-auth-badge.js — indicador de sesion/suscripcion en la cabecera.
 *
 * Rellena el placeholder <li id="bg-auth-status"></li> con un badge que refleja el estado
 * de sesion, y oculta el icono estatico de Login (<li id="bg-login-icon">, solo existe en
 * la plantilla raiz) cuando ya no hace falta.
 *
 * Nace porque hay suscriptores que ven las graficas recortadas (AVIV, M2...) sin darse
 * cuenta de que simplemente no han iniciado sesion en ese navegador.
 *
 * Fuentes de verdad, ambas cookies de dominio padre `.bgeometrics.com` emitidas por BGUser:
 *   - bgIsSubscriber() (bg-chart-data.js), lee `bg_full=1`: suscriptor de pago activo.
 *     Se reutiliza tal cual para que el badge y la banda naranja de las graficas
 *     (chart-upgrade-band.js) nunca puedan discrepar.
 *   - cookie `bg_user` (username URL-encoded): se emite en TODO login exitoso, sea cual sea
 *     el tier. Es la unica forma de detectar "logado" en JS, porque `bg_token` es HttpOnly.
 *
 * Estados:
 *   - Suscriptor (bg_full=1): oculta el icono de Login, pill verde con el username.
 *   - Logado pero no suscriptor (bg_user si, bg_full no): sin badge (no se ofrece login,
 *     ya esta logado) ni banda de upgrade en la cabecera — el icono de Login sigue visible
 *     por si quiere cambiar de cuenta.
 *   - Anonimo (ninguna cookie): pill ambar "Log in / Upgrade", icono de Login visible.
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

    var MAX_USERNAME_CHARS = 16;

    function getCookie(name) {
        var re = new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()\[\]\\/+^])/g, '\\$1') + '=([^;]*)');
        var m = document.cookie.match(re);
        if (!m || !m[1]) return null;
        try {
            return decodeURIComponent(m[1]);
        } catch (e) {
            return null;
        }
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function displayName(username) {
        var safe = escapeHtml(username);
        if (safe.length > MAX_USERNAME_CHARS) {
            return safe.slice(0, MAX_USERNAME_CHARS - 1) + '…';
        }
        return safe;
    }

    function setLoginIconVisible(visible) {
        var loginIcon = document.getElementById('bg-login-icon');
        if (loginIcon) {
            loginIcon.style.display = visible ? '' : 'none';
        }
    }

    function render() {
        var host = document.getElementById('bg-auth-status');
        if (!host) {
            return; // pagina sin cabecera (p.ej. un grafico embebido) → no hace nada
        }

        var isSub = (typeof bgIsSubscriber === 'function') && bgIsSubscriber();
        var username = getCookie('bg_user');
        var isLoggedIn = !!username;
        var isEs = (document.documentElement.lang || '').toLowerCase().indexOf('es') === 0;

        if (isSub) {
            setLoginIconVisible(false);
            // El .html de este href va dentro del JS, no de la plantilla, asi que no lo
            // toca el replace('.html', '_dark.html') del generador de paginas.
            // Fallback a "Subscriber"/"Suscriptor": sesiones emitidas antes de este cambio
            // tienen bg_full pero todavia no tienen bg_user.
            host.innerHTML =
                '<a href="' + PORTAL + '/dashboard.html" style="' + PILL +
                    'background:#10b981;" title="' +
                    (isEs ? 'Sesion iniciada — historico completo desbloqueado'
                          : 'Signed in — full history unlocked') + '">' +
                  '<i class="bi bi-patch-check-fill"></i>' +
                  '<span class="d-none d-md-inline">' +
                    (username ? displayName(username) : (isEs ? 'Suscriptor' : 'Subscriber')) +
                  '</span>' +
                '</a>';
            return;
        }

        setLoginIconVisible(true);

        if (isLoggedIn) {
            // Logado pero sin acceso completo (FREE): ya se le ha ofrecido iniciar sesion,
            // asi que no tiene sentido seguir mostrando el aviso de "Log in / Upgrade".
            host.innerHTML = '';
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
